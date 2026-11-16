#!/usr/bin/env python3
"""Pin and corner audit against device manuals, independent of the ECAD generator.

Run from anywhere. The pin table is transcribed as pad-number:net, not taken
from the generator's pin list. In the schematic we resolve *actual* gates,
device/pad connects and net/pinrefs, and in the routed board use contactrefs.
This tests connectivity intent at pads, not trace continuity, shorts, or EMC.
"""
from argparse import ArgumentParser
from itertools import product
import hashlib
import json
from math import log
from pathlib import Path
import re
from xml.etree import ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
# "-" requires a physically unconnected pad. Multiple pad numbers before a
# net represent intentionally paralleled pins; they are still checked one by one.
FOCUS = {
    'J101': 'A5:USB_CC1 B5:USB_CC2 A9,B9:VBUS A12,B12,SH1,SH2,SH3,SH4:GND',
    'D101': '1,6:USB_CC1 3,4:USB_CC2 2:GND 5:VBUS',
    'J102': '1:GND 2:BAT_NTC 3:VBAT',
    'J103': '1:PV_RAW 2:GND',
    'D102': '1:PV_IN 2:PV_RAW',
    'R126': '1:PV_IC_IN 2:PV_IN', 'C103': '1:PV_IC_IN 2:GND',
    'U101': '1:PV_MPP 2:PV_MPP_SET 3:PV_MPP_REF 4,5,6,13,18,EP:GND 7,11,12,17:- 8:PV_READY_N 9:PV_EOC 10:PV_UVP 14:PV_BUFFER 15:PV_STORE 16:PV_LVSW 19:PV_HVSW 20:PV_IC_IN',
    'Q101': '1:PV_READY_N 2:PV_STORE 3:PV_VALID',
    'U102': '1:BQ_TS 2,3:VBAT 4:CHG_DISABLE 5,6,8,EP:GND 7,9:- 10,11:SYS_AON 12:BQ_ILIM 13:CHG_IN 14:BQ_TMR 15:BQ_ITERM 16:BQ_ISET',
    'U103': '1:GND 2,7:CHG_IN 3,5:VBUS 4:USB_PR 6:PV_VALID 8:-',
    'U104': 'A1:MAIN_EN A2,A3:RT_VIN_LOCAL B1,C1,C2,C3:GND B2,B3:RT_SW1 D1:SCL D2,D3:RT_SW2 E1:SDA E2,E3:RT_VOUT_LOCAL',
    'R124':'1:RT_VIN_LOCAL 2:SYS_AON','R125':'1:RT_VOUT_LOCAL 2:VMAIN',
    'C113':'1:RT_VIN_LOCAL 2:GND','C114':'1:RT_VIN_LOCAL 2:GND',
    'C115':'1:RT_VOUT_LOCAL 2:GND','C116':'1:RT_VOUT_LOCAL 2:GND',
    'U105': '1:TEMP_COLD 2:NTC_COLD_REF 3,6:BAT_NTC 4:GND 5:NTC_HOT_REF 7:TEMP_HOT 8:CHG_IN',
    'D103':'1:TEMP_HOT 2:TEMP_COLD 3:CHG_DISABLE','R120':'1:CHG_DISABLE 2:GND',
    'R101': '1:USB_CC1 2:GND', 'R102':'1:USB_CC2 2:GND',
    'R103':'1:VBUS 2:USB_PR', 'R104':'1:USB_PR 2:GND',
    'R105':'1:PV_IC_IN 2:PV_MPP','R106':'1:PV_MPP 2:PV_MPP_SET','R107':'1:PV_MPP_SET 2:GND',
    'R108':'1:PV_STORE 2:PV_UVP','R109':'1:PV_UVP 2:PV_EOC','R110':'1:PV_EOC 2:GND',
    'R112':'1:BQ_TS 2:GND','R113':'1:BQ_ILIM 2:GND','R114':'1:BQ_TMR 2:GND',
    'R115':'1:BQ_ISET 2:GND','R123':'1:BQ_ITERM 2:GND',
    'R116':'1:CHG_IN 2:BAT_NTC','R117':'1:CHG_IN 2:NTC_COLD_REF',
    'R118':'1:NTC_COLD_REF 2:NTC_HOT_REF','R119':'1:NTC_HOT_REF 2:GND',
    'U201':'1:VBAT_MEAS_EN 3:SCL 4:SDA 7:VBAT_SENSE 9:VMAIN 10,30,31,37,38,39,40:GND 11:SWCLK 12:SWDIO 14:BTN2 15:BTN1 16:BTN3 18:EPD_DC 19:NRST 20:EPD_SCK 21:EPD_MOSI 22:EPD_RST 27:EPD_BUSY 28:EPD_CS 29:TIMER_DONE',
    'J201':'1:GND 2:VMAIN 3:SWCLK 4:SWDIO 5:NRST 6:WAKE_MDRV 7:VAON',
    'J301':'1,4,6,7:- 2:EPD_GDR 3:EPD_RESE 5:EPD_VSH2 8,17:GND 9:EPD_BUSY 10:EPD_RST 11:EPD_DC 12:EPD_CS 13:EPD_SCK 14:EPD_MOSI 15,16:VMAIN 18:EPD_VCORE 19:EPD_VPP 20:EPD_VSH1 21:EPD_VGH 22:EPD_VSL 23:EPD_VGL 24:EPD_VCOM',
    'Q301':'1:EPD_GDR 2:EPD_RESE 3:EPD_SW', 'D301':'1:GND 2:EPD_PUMP',
    'D302':'1:EPD_PUMP 2:EPD_VGL', 'D303':'1:EPD_VGH 2:EPD_SW',
    'U401':'1,3:SYS_AON 2:GND 4:- 5:VAON', 'U402':'1:VAON 2,6:GND 3:WAKE_MDRV 4:DONE_2V8 5:MAIN_EN',
    'U403':'1:RTC_XI 2:RTC_XO 3:RTC_IRQ_N 4:GND 5:SDA 6:SCL 7:- 8:VAON',
    'U404':'1,5,7:GND 2,6,8:VMAIN 3:SDA 4:SCL',
    'U405':'1:RTC_IRQ_N 2,3,10,11,16:VAON 4:RTC_PULSE_N 5,13:- 6,8,14:GND 7:KEY_MONO_RC 9:ANY_KEY_N 12:KEY_PULSE_N 15:RTC_MONO_RC',
    'Q401':'1:PULSE_GATE_N 2:VAON 3:WAKE_MDRV',
    'D401':'1:RTC_PULSE_N 2:KEY_PULSE_N 3:PULSE_GATE_N',
    'U406':'1:KEY1_N 2:KEY3_OUT 3:KEY2_N 4:GND 5:KEY2_OUT 6:KEY3_N 7:KEY1_OUT 8:VMAIN',
    'U407':'1:VBAT 2:GND 3:SENSE_SWITCH_EN 4:- 5,6:VBAT_ADC_SRC',
    'U408':'1,2:GND 3:MEAS_FILTER 4:SENSE_SWITCH_EN 5:VAON 6:MAIN_EN',
    'R420':'1:VBAT_ADC_SRC 2:VBAT_SENSE', 'R421':'1:VBAT_SENSE 2:GND',
    'R422':'1:VBAT_MEAS_EN 2:MEAS_FILTER', 'R423':'1:MEAS_FILTER 2:GND', 'R424':'1:SENSE_SWITCH_EN 2:GND',
    'C418':'1:MEAS_FILTER 2:GND',
}

def expected():
    return {(ref,pad):net for ref,row in FOCUS.items() for field in row.split()
            for nums,net in [field.split(':')] for pad in nums.split(',')}

def put(target, key, value):
    if key in target and target[key] != value:
        raise ValueError(f'{key}: conflicting nets {target[key]}, {value}')
    target[key] = value

def schematic_pads(path):
    root=ET.parse(path)
    comp={p.get('name'): p for p in root.findall('.//schematic/parts/part')}
    devices={(lib.get('name'),ds.get('name'),d.get('name','')):d for lib in root.findall('.//schematic/libraries/library')
             for ds in lib.findall('devicesets/deviceset') for d in ds.findall('devices/device')}
    pin_to_pad={r:{(c.get('gate'),c.get('pin')):c.get('pad').split()
                   for c in devices[(p.get('library'),p.get('deviceset'),p.get('device',''))].findall('connects/connect')} for r,p in comp.items()}
    padmap={}
    for net in root.findall('.//sheets/sheet/nets/net'):
        for pr in net.findall('.//pinref'):
            ref=pr.get('part')
            for pad in pin_to_pad[ref][(pr.get('gate'),pr.get('pin'))]:
                put(padmap,(ref,pad),net.get('name'))
    owned={(ref,p) for ref,d in pin_to_pad.items() for group in d.values() for p in group}
    # A device may deliberately omit a connect entry for a physical NC, e.g. a WLCSP.
    for ref, part in comp.items():
        dev=devices[(part.get('library'),part.get('deviceset'),part.get('device',''))]
        lib=root.find(f".//schematic/libraries/library[@name='{part.get('library')}']")
        pkg=lib.find(f"packages/package[@name='{dev.get('package')}']")
        if pkg is not None:
            owned.update((ref,p.get('name')) for p in list(pkg) if p.tag in ('pad','smd'))
    return owned,padmap

def board_pads(path):
    root=ET.parse(path)
    pack={(lib.get('name'),pkg.get('name')):pkg for lib in root.findall('.//board/libraries/library') for pkg in lib.findall('packages/package')}
    owned={(el.get('name'),pad.get('name')) for el in root.findall('.//board/elements/element')
           for pad in list(pack[(el.get('library'),el.get('package'))]) if pad.tag in ('pad','smd')}
    padmap={}
    for s in root.findall('.//board/signals/signal'):
        for p in s.findall('contactref'):
            put(padmap,(p.get('element'),p.get('pad')),s.get('name'))
    return owned,padmap

def audit_pads(owned,mapped):
    exp=expected()
    problems=[f'{ref}.{pad}: expected {net}, observed '+('missing pad' if (ref,pad) not in owned else mapped.get((ref,pad),'-'))
              for (ref,pad),net in exp.items() if (ref,pad) not in owned or net!=mapped.get((ref,pad),'-')]
    # A component across R126 would carry unmeasured panel current. The full
    # member sets also catch an added branch even if every listed pad is correct.
    pv_members = {}
    for net in ('PV_IN','PV_IC_IN'):
        actual={f'{ref}.{pad}' for (ref,pad),value in mapped.items() if value==net}
        required={f'{ref}.{pad}' for (ref,pad),value in exp.items() if value==net}
        pv_members[net]=sorted(actual)
        if actual!=required:
            problems.append(f'{net} unexpected members for the R126 series measurement: {sorted(actual^required)}')
    return {'pads_tested':len(exp),'devices_tested':len(FOCUS),'R126_terminal_net_members':pv_members,'errors':problems}

def resistance(parts, ref):
    v=parts[ref]['value']
    if '1%' not in v:
        raise ValueError(f'{ref}: 1% bound invalid: '+v)
    g=re.match(r'(\d+(?:\.\d+)?)\s*([MRk]?)',v)
    return float(g[1])*{'M':1e6,'k':1e3,'R':1,'':1}[g[2]]

def tol(v): return (v*.99,v*1.01)
def limits(seq):
    a=list(seq)
    return [round(min(a),7),round(max(a),7)]

def corners(parts):
    R=lambda i:resistance(parts,'R'+str(i))
    x,y,z=(R(i) for i in (108,109,110))
    lo,hi=limits(sum(r) for r in product(tol(x),tol(y),tol(z)))
    eoc=limits(v*(a+b+c)/c for v,a,b,c in product(tol(1.23),tol(x),tol(y),tol(z)))
    uvp=limits(v*(a+b+c)/(b+c) for v,a,b,c in product(tol(1.23),tol(x),tol(y),tol(z)))
    pv=limits((b+c)/(a+b+c) for a,b,c in product(*[tol(R(i)) for i in (105,106,107)]))
    mpp=limits(c/(b+c) for b,c in product(*[tol(R(i)) for i in (106,107)]))
    usb=limits(v*(a+b)/b+ileak*a for v,a,b,ileak in product((.92,1.08),tol(R(103)),tol(R(104)),(-.1e-6,.1e-6)))
    iset=limits(k/r for k,r in product((797,975),tol(R(115))))
    iterm=limits(k*a/b for k,a,b in product((.008,.012),tol(R(123)),tol(R(115))))
    tfast=limits(10*k*(r/1000)/3600 for k,r in product((36,60),tol(R(114))))
    adc=limits(4.2*2*b/(a+b)-4.2 for a,b in product(tol(R(420)),tol(R(421))))
    ntc={'cold':[],'hot':[]}
    # Full independent endpoints: resistors and R25 1%, beta ±2% assumed
    # to guard unspecified supplier B tolerance, input trip error ±20mV
    # at minimum BQ UVLO 3.2V; same ratio at either charging source.
    for up,a,b,c,r25,beta,trip in product(*[tol(R(i)) for i in (116,117,118,119)],tol(10000),(3435*.98,3435*1.02),(-.020,.020)):
        for name,ratio in [('cold',(b+c)/(a+b+c)),('hot',c/(a+b+c))]:
            f=ratio+trip/3.2
            rt=up*f/(1-f)
            ntc[name].append(1/(1/298.15+log(rt/r25)/beta)-273.15)
    cold,hot=(limits(ntc[i]) for i in ('cold','hot'))
    check={'PV current link is the fitted Panasonic 1 A zero-ohm part':parts['R126']['mpn']=='ERJ3GEY0R00V' and parts['R126']['value'].startswith('0R 1A'),
           'SPV output ladder 10 to 20 MΩ inclusive':lo>=10e6 and hi<=20e6,
           'SPV EOC within 2.6 to 5.3V; solar restarts above maximum BQ VIN-DPM, typical hysteresis':eoc[1]<=5.3 and eoc[0]*.99>4.63,
           'SPV UVP in 2.2 to 3.6V and separated from EOC':2.2<=uvp[0] and uvp[1]<=3.6 and uvp[1]*1.05 < eoc[0]*.99,
           'Mux at a valid USB port voltage selects USB':usb[1]<4.75,
           'BQ ISET standard range and under pack 125 mA without USB100 clamp':tol(R(115))[0]>=590 and tol(R(115))[1]<=8900 and iset[1]<.125,
           'BQ programmed safety timer range and termination below charging current':18e3<tol(R(114))[0] and tol(R(114))[1]<72e3 and 0<iterm[0]<iterm[1]<iset[0],
           'Both connector CC have separate 5.1k ±1% sink resistors':R(101)==R(102)==5100,
           'NTC guard band, at stated error bounds, stays inside pack 10..45°C':cold[0]>10 and hot[1]<45 and cold[1]<25<hot[0],
           'Divider tolerance alone <50mV at 4.2V before ADC error':max(abs(i) for i in adc)<.05}
    return {'checks':check,'SPV_total_output_resistance_ohm':[lo,hi],'SPV_EOC_V':eoc,'SPV_UVP_V':uvp,
            'MPP_fraction_of_harvester_open_circuit_V':pv,'MPPT_fraction_of_Voc':mpp,
            'highest_PV_IN_Voc_at_all_resistor_corners_for_2p1V_MPP':round(2.1/pv[1],4),
            'USB_takeover_V_including_PR1_100nA':usb,'ISET_A_before_USB100':iset,
            'USB100_ITERM_A':iterm,'BQ_fast_timer_h_not_in_DPM':tfast,
            'NTC_cold_trip_C_range':cold,'NTC_hot_trip_C_range':hot,
            'ADC_error_V_resistors_only_at_4p2V':adc}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def native_stack(board):
    """Check constructed layers/side, not only the layer declarations."""
    from collections import Counter
    params={p.get('name'):p.get('value') for p in board.findall('designrules/param')}
    mm=lambda s:float(s.removesuffix('mm')) if s.endswith('mm') else float('nan')
    foils=list(map(mm,params['mtCopper'].split()));core=mm(params['mtIsolate'].split()[0])
    layers={name:dict(Counter(i.get(key,'') for i in board.findall('signals/signal/'+name)))
            for name,key in [('wire','layer'),('polygon','layer'),('via','extent')]}
    parts=board.findall('elements/element')
    mirrored=[p.get('name') for p in parts if 'M' in p.get('rot','')]
    used={(p.get('library'),p.get('package')) for p in parts}
    bottom_smd=[f"{lib.get('name')}/{pkg.get('name')}/{p.get('name')}" for lib in board.findall('libraries/library')
                for pkg in lib.findall('packages/package') if (lib.get('name'),pkg.get('name')) in used
                for p in pkg.findall('smd') if p.get('layer')!='1']
    thickness=round(foils[0]+core+foils[15],4)
    checks={'Native two-sided stack selector is (1*16)':params['layerSetup']=='(1*16)',
            'Native foil + dielectric + foil nominal 1.00mm':abs(thickness-1)<.0001,
            'All actual signal traces, pours and plated vias are two-layer features':
              set(layers['wire'])=={'1','16'} and set(layers['polygon'])=={'1','16'} and set(layers['via'])=={'1-16'},
            'Every fitted or board-feature placement faces top and every SMD in used packages is top':not mirrored and not bottom_smd}
    return {'checks':checks,'elements':len(parts),'mirrored_elements':mirrored,'non_top_smds':bottom_smd,
            'native_stack_foil_dielectric_foil_mm':[foils[0],core,foils[15]],'foil_to_foil_nominal_mm':thickness,'routed_layer_uses':layers}

def main():
    ap=ArgumentParser(description=__doc__)
    ap.add_argument('--project',type=Path,default=ROOT)
    ap.add_argument('--require-board',action='store_true')
    ap.add_argument('--output',type=Path,default=HERE/'design-review.json')
    args=ap.parse_args();work=args.project
    vals={}
    for subsystem in ('power','wake','radio','display'):
        path=work/'hardware'/f'{subsystem}.json'
        vals.update({p['ref']:p for p in json.loads(path.read_text())['parts']})
    evals=corners(vals)
    summary={'method':'Independent analysis of physical pad nets from native XML. No generator code imported.',
             'scope':'Selected high-risk physical pad checks and closed-form limits; trace continuity and parasitics require separate verification.',
             'corners':evals}
    errors=[k for k,v in evals['checks'].items() if not v]
    for name, path, fn in [('schematic',work/'schematic/astra.sch',schematic_pads),('board',work/'board/astra.brd',board_pads)]:
        if path.is_file():
            record=audit_pads(*fn(path));record['sha256']=sha(path);record['path']=str(path.relative_to(work))
            tree=ET.parse(path)
            if name=='board':
                stack=native_stack(tree.find('.//board'));record['construction']=stack
                record['errors'] += [key for key,value in stack['checks'].items() if not value]
            items={p.get('name'):p for p in tree.findall('.//schematic/parts/part' if name=='schematic' else './/board/elements/element')}
            # SPICE/corner values must match the hardware actually delivered.
            for ref in FOCUS:
                if ref not in items: continue  # reported by pin audit
                item=items[ref]
                if item.get('value')!=vals[ref]['value']:
                    record['errors'].append(f"{ref}: native value {item.get('value')} disagrees with {vals[ref]['value']}")
                mpn=item.find("attribute[@name='MPN']")
                if mpn is not None and mpn.get('value')!=vals[ref]['mpn']:
                    record['errors'].append(f"{ref}: native MPN {mpn.get('value')} disagrees with {vals[ref]['mpn']}")
            summary[name]=record
            errors += [name+' '+p for p in record['errors']]
        else:
            summary[name]={'status':'not present, not checked'}
            if name!='board' or args.require_board: errors.append(f'{name} missing')
    summary['errors']=errors
    summary['status']='FAIL' if errors else ('PASS' if 'sha256' in summary['board'] else 'PASS schematic/corners; board not yet available')
    args.output.write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
    print(summary['status'])
    if errors: print('\n'.join(errors))
    raise SystemExit(bool(errors))

if __name__=='__main__': main()
