#!/usr/bin/env python3
"""Exercise TI's untouched TPS2116 transistor/behavioral macro-model in ngspice PSpice mode."""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from urllib.request import Request, urlopen
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
MODEL = 'https://www.ti.com/lit/zip/SLVMDI4'
ARCHIVE_SHA = '730dd922475b68183cb2d3ecac3259c8f5637e6458764ced7f3fbc0c89da80a7'
LIB_SHA = '3c111bb702f86d7c3abf957e24f565651e534e4cdac40799b210b8ec1358ea18'
CASES = [('threshold_nominal', '1u', '.001'), ('threshold_tighter', '1u', '.0008'),
         ('threshold_half_step', '.5u', '.001')]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_model(archive):
    raw = archive.read_bytes() if archive else urlopen(Request(MODEL, headers={'User-Agent':'Mozilla/5.0'}),timeout=35).read()
    if sha(raw) != ARCHIVE_SHA:
        raise ValueError('TI model archive changed. Review version before running.')
    with ZipFile(io.BytesIO(raw)) as z:
        lib = z.read('TPS2116_PSPICE_TRANS/TPS2116_TRANS.LIB')
    if sha(lib) != LIB_SHA:
        raise ValueError('Unexpected TI library.')
    return lib


def run(name, max_step, reltol, sim, lib):
    deck = (HERE/'switch.cir').read_text().replace('@step@',max_step).replace('@reltol@',reltol)
    with tempfile.TemporaryDirectory() as directory:
        work=Path(directory)
        (work/'ti.lib').write_bytes(lib)
        (work/'.spiceinit').write_text('set ngbehavior=ps\n')
        (work/'switch.cir').write_text(deck)
        result=subprocess.run([sim,'-b','switch.cir'],cwd=work,capture_output=True,text=True,timeout=90)
        log=result.stdout+'\n'+result.stderr
        (HERE/(name+'.log')).write_text(log)
        if result.returncode or re.search(r'aborted|failed|Error:|Timestep too small',log,re.I):
            raise RuntimeError(name+' did not complete. See its log.')
        values={k:float(v) for k,v in re.findall(r'(?m)^(usb_initial|usb_active|solar_after|transient_min|last_point)\s*=\s*([\d.+eE-]+)',log)}
        if len(values)!=5 or not (5.15<values['usb_initial']<5.26 and 5.15<values['usb_active']<5.26 and 4.93<values['solar_after']<5.05 and 4.93<values['last_point']<5.05):
            raise RuntimeError(name+' missed expected DC bounds.')
        trace=[]
        for line in (work/'trace.txt').read_text().splitlines():
            t,usb,pv,pr,vout=map(float,line.split())
            if .00798 <= t <= .00845:
                trace.append([t,usb,pv,pr,vout])
        with (HERE/(name+'.csv')).open('w',newline='') as f:
            w=csv.writer(f);w.writerow(['time_s','usb_at_mux_V','solar_at_mux_V','PR1_V','charger_input_V']);w.writerows(trace)
        return dict(name=name,reltol=reltol,max_step=max_step,**values)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive',type=Path,help='Previously downloaded TI SLVMDI4A.zip')
    args=parser.parse_args()
    sim=shutil.which('ngspice') or '/opt/homebrew/bin/ngspice'
    lib=read_model(args.archive)
    cases=[run(*case,sim,lib) for case in CASES]
    worst=min(e['transient_min'] for e in cases); best=max(e['transient_min'] for e in cases)
    if best-worst > .020:
        raise AssertionError('The supply handoff did not reproduce within 20 mV between solver settings.')
    meta=dict(source=MODEL,model_version='TI TPS2116 Final 1.10 / SLVMDI4A',
              archive_sha256=ARCHIVE_SHA,library_sha256=LIB_SHA,
              simulator=subprocess.run([sim,'--version'],capture_output=True,text=True).stdout.strip(),cases=cases,
              comparison='VBUS-to-PV minimum following steady-state USB agrees within 20mV across 3 runs.',
              fixture='Both inputs valid initially; solar equivalent 5.01111V (6.8M/1.5M/2.7M EOC); source resistance 0.5 ohm per rail, DC 180 ohm load, VOUT 3.5uF effective, 55 milliohm capacitor ESR, 1uF USB; ngspice default 27°C.',
              exclusions=['The circuit is initialized at its DC operating point with valid USB and valid solar. With the cold-start variant, ngspice can converge to inconsistent starting branches; this run is not a startup validation.',
                          'TI removed diode-mode behavior from this model. With MODE=VBUS=0 it cannot validate the physical highest-input fallback.',
                          'BQ24074, cell, SPV1050 harvesting dynamics, temperature and source parasitics beyond the stated test fixture are outside this model.'])
    (HERE/'results.json').write_text(json.dumps(meta,indent=2)+'\n')
    print('USB→solar charger-input minimum range',f'{worst:.4f}…{best:.4f} V')


if __name__=='__main__':
    main()
