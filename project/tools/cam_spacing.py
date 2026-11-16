"""Evaluate the JLC Standard PCBA component/terminal edge spacing matrix."""
from itertools import combinations
from shapely import affinity, union_all
from shapely.geometry import box


CHIPS = ('0402','0603','0805','1206')
CLASSES = (*CHIPS,'QFN','SOP','SOT','BGA')
# Symmetric upper triangle of JLC's September 2026 published matrix, mm.
TABLE = ((.15,.18,.18,.25,1,.4,.2,1), (.18,.18,.25,1,.4,.2,1),
         (.18,.25,1,.4,.2,1), (.35,1,.4,.2,1), (1,1,1,1.5), (.5,.4,1), (.4,1), (2,))
VARIANTS = {
    'TI_RGT16_BQ74':'QFN', 'SPV_VFQFPN20':'QFN', 'RT_WLCSP15':'BGA', 'BOSCH_BME280':'QFN',
    'MC_MSOP8_TEMP':'SOP', 'NXP_TSSOP16_MONO':'SOP', 'NXP_SO8_RTC':'SOP', 'TI_DCU8_KEY':'SOP',
    'TI_DRL8_MUX':'SOT', 'TI_DCK6_SENSE':'SOT', 'ST_SOT23_6_ESD':'SOT', 'NXP_SOT23_DIODE':'SOT',
    'SOT23_AO3401A':'SOT', 'SOT23_WAKE':'SOT', 'TI_DDC6_TPL':'SOT', 'TI_DBV5_W':'SOT', 'BSS138_CASE318':'SOT'}


def assembly_spacing(parts, bodies, lands):
    fp_class = {ref: next((size for size in CHIPS if size in part['footprint']),VARIANTS.get(part['footprint'])) for ref,part in parts.items()}
    grouped = {ref: [] for ref in bodies}
    for (ref,_),land in lands.items():
        if ref in grouped:
            grouped[ref].append(land)
    envelopes = {ref: union_all([shape,*grouped[ref]]) for ref,shape in bodies.items()}
    checks = 0
    margins = {}
    violations = []
    unclassified = {}
    for a,b in combinations(bodies,2):
        ca,cb = fp_class[a],fp_class[b]
        gap = envelopes[a].distance(envelopes[b])
        body_gap = bodies[a].distance(bodies[b])
        if ca is None or cb is None:
            for ref,near in ((a,b),(b,a)):
                if fp_class[ref] is None and (ref not in unclassified or gap < unclassified[ref]['gap_mm']):
                    unclassified[ref] = {'package':parts[ref]['footprint'],'nearest_part':near,'gap_mm':round(gap,5),'body_gap_mm':round(body_gap,5)}
            continue
        checks += 1
        i,j = sorted([CLASSES.index(ca),CLASSES.index(cb)])
        minimum = TABLE[i][j-i]
        name = CLASSES[i] + ' / ' + CLASSES[j]
        row = {'refs':[a,b], 'required_mm':minimum, 'body_and_terminal_gap_mm':round(gap,5), 'body_only_gap_mm':round(body_gap,5)}
        if name not in margins or gap < margins[name]['body_and_terminal_gap_mm']:
            margins[name] = row
        if gap < minimum - .001:
            violations.append(row)
    return {'source':'https://jlcpcb.com/help/article/minimum-spacing-for-smd-components',
            'method':'Placed body united with its plotted numbered copper lands, including protruding toe. WLCSP treated as BGA and BME LGA as QFN. Unlisted packages record nearest envelope separately.',
            'table_pairs_checked':checks,'class_minima':margins,'table_violations':violations,'unlisted_package_nearest':unclassified}


def boost_package_tolerance(entries, lands, apertures):
    # Maximum as-built XY outlines from onsemi CASE 318 AU and Bourns SRN4018.
    # Compare to actual pasted lands, including the immediately adjacent switch node.
    maxima={'Q301':(3.04,1.40),'L301':(4.20,4.20)}
    output={}
    for ref,(w,h) in maxima.items():
        if ref not in entries:continue
        data=entries[ref];cx,cy=data['xy'];orientation=float(data['element'].get('rot','R0').split('R')[-1])
        maximum=affinity.rotate(box(cx-w/2,cy-h/2,cx+w/2,cy+h/2),orientation,origin=(cx,cy))
        own=union_all([g for (r,_),g in lands.items() if r==ref])
        outside=[ap for ap in apertures if not ap.intersects(own)]
        nearest=min(outside,key=maximum.distance)
        distance=maximum.distance(nearest)
        # 50 µm position error on EACH Cartesian axis is a project qualification
        # envelope for first-article SPI/AOI, not a claimed vendor machine rating.
        from shapely.affinity import translate
        worst=union_all([translate(maximum,dx,dy) for dx,dy in [(-.05,-.05),(-.05,.05),(.05,-.05),(.05,.05)]]).convex_hull
        overlap=sum(worst.intersection(ap).area for ap in outside if worst.intersects(ap))
        output[ref]={'max_body_xy_mm':[w,h],'assembly_xy_tolerance_assumption_mm':.05,
                     'nearest_foreign_paste_contacts':[r+'.'+p for (r,p),g in lands.items() if g.intersects(nearest)],
                     'max_body_to_paste_mm':round(distance,5),'with_placement_to_paste_mm':round(min(worst.distance(ap) for ap in outside),5),
                     'with_placement_paste_overlap_mm2':round(overlap,7),'pass':overlap<.00001 and min(worst.distance(ap) for ap in outside)>.001}
    return output
