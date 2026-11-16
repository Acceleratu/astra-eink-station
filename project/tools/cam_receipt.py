#!/usr/bin/env python3
"""Bind automated manufacturing checks to the source revision and shipped outputs."""
from collections import Counter
import csv
import gzip
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

from cam_stock import ROOT


FAB = ROOT / 'fab'
VERIFY = ROOT / 'verification/manufacturing'


def json_file(path):
    return json.loads(path.read_text())


def csv_file(path):
    with path.open(newline='') as file:
        return list(csv.DictReader(file))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    board_hash = sha(ROOT/'board/astra.brd')
    geometry = json_file(VERIFY/'gerber-vs-native.json')
    drc = json_file(VERIFY/'independent-drc.json')
    imported = json_file(VERIFY/'independent-board/import.json')
    spacing = json_file(VERIFY/'assembly/body-terminal-spacing.json')
    probes = json_file(VERIFY/'assembly/probe-access.json')
    placements = json_file(VERIFY/'assembly/placement-vs-import.json')
    dft_inputs = json_file(VERIFY/'assembly/assembly-geometry-inputs.json')
    rotation = json_file(VERIFY/'assembly/rotation-review.json')
    stock = csv_file(VERIFY/'stock/availability.csv')
    bom = csv_file(FAB/'BOM-JLCPCB.csv')
    cpl = csv_file(FAB/'CPL-JLCPCB.csv')
    fitted = csv_file(VERIFY/'assembly/fitted-parts.csv')
    inventory = json_file(VERIFY/'stock/details.json')
    expected = {d for r in bom for d in r['Designator'].split(',')}
    inputs = {r['JLCPCB part']:r for r in stock}
    source_identity = {code:(r['Design MPN'],r['Official MPN']) for code,r in inputs.items()}
    checksum_errors = [c for c,r in inventory.items() if not r.get('response_sha256') or
                        hashlib.sha256(gzip.decompress((VERIFY/'stock'/f'{c}.json.gz').read_bytes())).hexdigest()!=r['response_sha256']]
    short_stock = [r['JLCPCB part'] for r in stock if not r['Stock'] or not r['Conservative feed quantity'] or
                   int(r['Stock']) < int(r['Conservative feed quantity'])]
    no_prepurchase = [(r['JLCPCB part'],r['Stock'],r['Available order quantity (parts library)']) for r in stock
                      if int(r['Available order quantity (parts library)']) < int(r['Conservative feed quantity'])]
    checks = {}

    def check(name, passed, measured):
        checks[name] = {'pass':bool(passed),'result':measured}

    check('native_board_sha',board_hash==geometry['source_sha256']==placements['source_sha256']==dft_inputs['native_sha256'] and
          all(geometry['file_sha256'].get(k)==v for k,v in dft_inputs['plot_sha256'].items()) and
          all(v==sha((VERIFY/'assembly' if k.endswith('.json') else FAB)/k) for k,v in dft_inputs['result_sha256'].items()),board_hash)
    check('native_import',not imported['errors'] and not imported['warnings'],{'errors':imported['errors'],'warnings':imported['warnings']})
    check('independent_DRC',not drc['violations'] and not drc['unconnected_items'],
          {'violations':dict(Counter(v['type'] for v in drc['violations'])),'unconnected_entries':len(drc['unconnected_items'])})
    for key in ('missing_native_drills','extra_plot_drills','missing_plated_annulus','missing_copper_at_pads','via_net_mismatches',
                'shorted_nets_from_copper','open_nets_from_copper','missing_x2_pad_attributes','shifted_x2_pad_centers','merged_top_mask_openings'):
        check(key,not geometry[key],geometry[key])
    tracks=geometry['track_centerlines'];check('native_vs_Gerber_conductors',not tracks['differences'],tracks)
    outline=geometry['outline_comparison'];check('profile',outline['native_contours']==outline['gerber_contours']==1 and outline['boundary_hausdorff_mm']<.002,outline)
    job=geometry['job_specifications'];xmin,ymin,xmax,ymax=geometry['native_outline_centerline_bounds_mm']
    job_proof=json_file(VERIFY/'gerber-job-provenance.json')
    check('published_Gerber_job',job['Size']=={'X':xmax-xmin,'Y':ymax-ymin} and job['ProjectId']['Revision']=='A' and job['Finish']=='ENIG' and
          job['BoardThickness']==1 and job['LayerNumber']==2 and job_proof['native_sha256']==board_hash and
          len(job_proof['individual_Gerber_X2_revisions'])==8 and set(job_proof['individual_Gerber_X2_revisions'].values())=={'A'} and
          job_proof['shipped_job_sha256']==sha(next((FAB/'Gerbers').glob('*.gbrjob'))),job)
    for side,bounds in geometry['copper_to_gerber_outline'].items():
        check(side+'_copper_edge',bounds['distance_to_milled_edge_mm']>=.35-.001 and bounds['copper_outside_profile_area_mm2']==0,bounds)
    for key,value in geometry['manufactured_spacing'].items():check(key,not value['violations'],value)
    for side,value in geometry['mask_to_foreign_copper'].items():check(side+'_mask_to_foreign_copper',not value['violations'],value)
    check('drill_spacing',not geometry['drill_spacing']['violations'],geometry['drill_spacing'])
    check('silk_to_mask',geometry['top_silk_to_mask_distance_mm']>=.15,round(geometry['top_silk_to_mask_distance_mm'],5))
    zones=geometry['stencil_step_zones'];ar=geometry['minimum_stencil_area_ratio']
    check('stepped_stencil',len(zones)==2 and min(z['closest_aperture_to_step_mm'] for z in zones)>=1.5 and ar>=.66,
          {'steps':zones,'paste_openings':len(geometry['stencil_apertures']),'minimum_area_ratio':ar})
    check('component_terminal_spacing',not spacing['table_violations'],{'classified_pairs':spacing['table_pairs_checked'],'violations':spacing['table_violations']})
    worst_case=spacing['boost_max_case_to_foreign_paste'];check('max_boost_package_to_foreign_paste',len(worst_case)==2 and all(v['pass'] for v in worst_case.values()),worst_case)
    check('top_probe_access',all(p['status']=='PASS' for p in probes),{'points':len(probes),'flags':[p for p in probes if p['status']!='PASS']})
    links=csv_file(FAB/'measurement-links.csv')
    check('current_measurement_links',{row['Designator'] for row in links}=={'R124','R125','R126'} and all(row['Pad 1 net']!=row['Pad 2 net'] for row in links),links)
    check('CPL_reference_set_and_side',expected=={r['Designator'] for r in cpl} and len(expected)==len(cpl)==placements['compared_rows'] and
          all(r['Layer']=='Top' for r in cpl),{'fitted':len(cpl),'independently_compared':placements['compared_rows']})
    tallest=max(fitted,key=lambda r:float(r['Height mm']))
    check('published_TOP_height',float(tallest['Height mm'])<=4.1 and all(float(f['Height mm'])>0 for f in fitted),
          {'tallest':tallest['Designator'],'maximum_component_envelope_mm':float(tallest['Height mm']),'project_limit_mm':4.1})
    check('rotation_evidence',all(v['rotation_from_catalog_deg'] is not None and 'matched' in v['assessment'] for v in rotation.values()),
          dict(Counter(v['assessment'] for v in rotation.values())))
    check('live_stock_coverage',len(inventory)==len(inputs) and not checksum_errors and not short_stock and all(
          sources[0].casefold()==sources[1].casefold() for sources in source_identity.values()) and
          {r['LCSC Part #'] for r in bom}==set(inventory) and all(source_identity[r['LCSC Part #']][0]==r['Manufacturer Part Number'] for r in bom),
          {'codes':len(inputs),'sample_boards':int(stock[0]['Sample build quantity']),'insufficient_SMT_stock':short_stock,
           'parts_library_prebuy_below_allowance':no_prepurchase,'raw_hash_errors':checksum_errors,
           'retrieved_utc':[min(r['Retrieved UTC'] for r in stock),max(r['Retrieved UTC'] for r in stock)]})
    filenames={f.name for f in (FAB/'Gerbers').iterdir() if f.is_file()}
    with ZipFile(FAB/'astra-Gerber-drill.zip') as archive:
        archived={name:hashlib.sha256(archive.read(name)).hexdigest() for name in archive.namelist()}
    fresh_plots=all(sha(FAB/'Gerbers'/f)==v for f,v in geometry['file_sha256'].items())
    check('fabrication_zip',fresh_plots and filenames==set(archived) and all(sha(FAB/'Gerbers'/f)==h for f,h in archived.items()),archived)
    stats={k:geometry[k] for k in ('native_pad_count','native_signal_count','native_vias_compared','reopened_drill_count','drill_coordinate_comparison','job_specifications')}
    report={'native_board_sha256':board_hash,'automated_checks_passed':all(r['pass'] for r in checks.values()),'native_and_CAM_counts':stats,'checks':checks,
            'KiCad_builtin_optional_checks_disabled_by_default':drc['ignored_checks'],
            'assembly_process_records':['SPI paste volume','AOI and WLCSP X-ray','post-reflow height','fixture fit','functional and RF bench tests'],
            'physical_tests_status':'Unexecuted. No populated board, stencil or instruments supplied.',
            'fabrication_and_assembly_outputs':{p.name:sha(p) for p in sorted(FAB.iterdir()) if p.is_file()}}
    (VERIFY/'final-checks.json').write_text(json.dumps(report,indent=2)+'\n')
    failed=[name for name,v in checks.items() if not v['pass']]
    status='TRECE' if not failed else 'NECESITĂ CORECȚII'
    closest_mask=geometry['manufactured_spacing']['solder_mask_web']['minimum_within_search_radius_mm']
    low_stock=' / '.join(f"{code} = {on_hand} pe stoc, {buy} disponibile pentru precumpărare" for code,on_hand,buy in no_prepurchase) or 'Toate codurile acoperă și precumpărarea.'
    cells=checks['max_boost_package_to_foreign_paste']['result']
    summary=f'''# Verificarea fabricației, revizia {job['ProjectId']['Revision']}

**{status}** la {len(checks)-len(failed)} din {len(checks)} controale executabile. Placa EAGLE verificată are SHA256 `{board_hash}`. Raportul complet conține hashurile fișierelor trimise pentru prototip. [Rezultate și hashuri](final-checks.json)

| Măsurare | Rezultat pe revizia verificată |
|---|---|
| Import EAGLE și DRC KiCad 10.0.8 | {len(imported['errors'])} erori și {len(imported['warnings'])} avertismente la import. {len(drc['violations'])} încălcări DRC și {len(drc['unconnected_items'])} conexiuni rămase |
| Continuitate din cuprul Gerber după găurire | {stats['native_signal_count']} rețele, {stats['native_pad_count']} terminale, {len(geometry['shorted_nets_from_copper'])} grupuri în scurt și {len(geometry['open_nets_from_copper'])} rețele întrerupte |
| Trasee și vias | {tracks['native_segments']} segmente în sursă, {tracks['gerber_segments']} pe film, {len(tracks['differences'])} diferențe de axă sau lățime. {stats['native_vias_compared']} vias verificate individual |
| Excellon | {geometry['drill_coordinate_comparison']['matched_one_to_one']} găuri asociate individual. Eroare maximă pe axă {geometry['drill_coordinate_comparison']['maximum_axis_quantization_mm']:.4f} mm |
| Profil și straturi | {job['Size']['X']:.2f} × {job['Size']['Y']:.2f} mm pe axa frezei. {job['LayerNumber']} straturi, {job['BoardThickness']:.2f} mm, {job['Finish']}. Diferență de arie între profiluri {outline['symmetric_difference_mm2']:.5f} mm² |
| Cupru față de contur | TOP {geometry['copper_to_gerber_outline']['top']['distance_to_milled_edge_mm']:.3f} mm, BOTTOM {geometry['copper_to_gerber_outline']['bottom']['distance_to_milled_edge_mm']:.3f} mm |
| Mască și serigrafie | Punte minimă {closest_mask:.3f} mm. Serigrafie TOP până la deschidere {geometry['top_silk_to_mask_distance_mm']:.3f} mm |
| Stencil | {len(geometry['stencil_apertures'])} aperturi, raport minim de arie {ar:.4f}. Distanță minimă de la trepte la o apertură {min(z['closest_aperture_to_step_mm'] for z in zones):.2f} mm |
| Montaj | {len(cpl)} plasări TOP, {len(inventory)} MPN-uri, {len(rotation)} perechi de cod și footprint cu orientarea documentată. Înălțime maximă de proiect {float(tallest['Height mm']):.2f} mm la {tallest['Designator']} |
| Acces și toleranțe | {spacing['table_pairs_checked']} perechi în matricea de montaj JLC, {len(spacing['table_violations'])} observații. Cu piesele la dimensiunea maximă și cu eroarea de poziționare presupusă ±0,05 mm pe axă, Q301 rămâne la {cells['Q301']['with_placement_to_paste_mm']:.3f} mm și L301 la {cells['L301']['with_placement_to_paste_mm']:.3f} mm de pasta celorlalte piese |
| Puncte de probă | {len(probes)} contacte. Cupru expus ≥{min(p['exposed_inscribed_diameter_mm'] for p in probes):.2f} mm, acces până la corp ≥{min(p['body_edge_clearance_mm'] for p in probes):.3f} mm, distanță până la muchie ≥{min(p['land_to_board_edge_mm'] for p in probes):.2f} mm, pas ≥{min(p['nearest_probe_pitch_mm'] for p in probes):.2f} mm |

Interogările JLC au avut loc între `{checks['live_stock_coverage']['result']['retrieved_utc'][0]}` și `{checks['live_stock_coverage']['result']['retrieved_utc'][1]}`. S-au evaluat două prototipuri cu rezerva pentru alimentator. Codurile cu deficit la alimentarea liniei sunt consemnate în registru ({', '.join(short_stock) if short_stock else 'niciunul'}). Pentru achiziția anticipată în biblioteca proprie, registrul indică {low_stock}. Stocul rămâne nealocat până la o comandă. [Răspunsuri individuale de catalog](stock/availability.csv)

Sursele brute includ importul, DRC, straturile redeschise, geometria de lipire și accesul la probe. Inspecția plăcii fabricate, SPI, AOI, X-ray, înălțimea măsurată și funcționarea electrică și RF rămân probe fizice neexecutate. [Import](independent-board/import.json) · [DRC](independent-drc.json) · [Comparație cu Gerber](gerber-vs-native.json) · [Toleranțe de montaj](assembly/body-terminal-spacing.json) · [Probe](assembly/probe-access.json) · [Planul de calificare](../../docs/qualification.md)
'''
    (VERIFY/'summary.md').write_text(summary)
    print(f'{len(checks)-len(failed)}/{len(checks)} executable checks passed. Failed: {failed}')
    return bool(failed)


if __name__=='__main__':
    raise SystemExit(main())
