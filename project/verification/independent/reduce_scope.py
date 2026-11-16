#!/usr/bin/env python3
"""Reduce an actual synchronized battery/rail log, without assuming uniform sampling.

CSV header: time_s,vbat_V,ibat_A,vmain_V. Positive current leaves the battery.
No supplied trace is a board measurement. The --self-test fixture is synthetic.
"""
import argparse
import csv
import json
import math
import sys
from pathlib import Path

def test_windows(rows,max_gap_s):
    first=None;prev=None;last_awake=None;charge=returned=energy=awake=0.
    sample_count=0;max_gap=0.;peak_d=-math.inf;peak_c=-math.inf;hist={};off_time=0.;off_ua_s=0.
    for point in rows:
        t,v,i,vm=point
        if not all(math.isfinite(x) for x in point) or v<0 or vm<-.2:
            raise ValueError(f'invalid sample: {point}')
        peak_d=max(i,peak_d);peak_c=max(-i,peak_c);sample_count+=1
        if prev is None:
            first=last_awake=t;prev=point;continue
        t0,v0,i0,vm0=prev;dt=t-t0
        if dt<=0 or dt>max_gap_s:
            raise ValueError(f'nonmonotone or excessive gap at t={t}, dt={dt}; allowed 0<dt<={max_gap_s}')
        max_gap=max(max_gap,dt)
        # Integrate a piecewise-linear current. Split polarity changes at i=0.
        if i*i0<0:
            crossing=dt*(-i0)/(i-i0)
            charge+=max(0.,i0)*crossing/2+max(0.,i)*(dt-crossing)/2
            returned+=max(0.,-i0)*crossing/2+max(0.,-i)*(dt-crossing)/2
        else:
            charge+=max(0.,(i+i0)*dt/2)
            returned+=max(0.,-(i+i0)*dt/2)
        # Integral of the product of two linear interpolants (V and I).
        dv=v-v0;di=i-i0
        energy+=dt*(v0*i0+(v0*di+i0*dv)/2+dv*di/3)
        if vm>.3 or vm0>.3:
            last_awake=t;awake+=dt
        else:
            # Discard the first 10 s of a contiguous interval under 0.30 V.
            span=max(0., t-max(t0,last_awake+10))
            if span>0:
                level0=i-di*span/dt
                mean_ua=(level0+i)*.5e6;bucket=round(mean_ua)
                hist[bucket]=hist.get(bucket,0.)+span;off_ua_s+=mean_ua*span;off_time+=span
        prev=point
    if sample_count<2:raise ValueError('at least two data rows required')
    median=None;cumulative=0.
    for value in sorted(hist):
        cumulative+=hist[value]
        if cumulative>=off_time/2:
            median=value;break
    return dict(samples=sample_count,duration_s=prev[0]-first,max_sampling_gap_s=max_gap,
                battery_discharge_mAh=charge/3.6,battery_charge_returned_mAh=returned/3.6,
                battery_net_discharge_mAh=(charge-returned)/3.6,battery_net_energy_mWh=energy/3.6,
                sampled_peak_discharge_mA=1000*max(0,peak_d),sampled_peak_charge_mA=1000*max(0,peak_c),
                rail_awake_interval_envelope_s=awake,qualified_sleep_s=off_time,
                sleep_time_weighted_mean_uA=(off_ua_s/off_time if off_time else None),
                sleep_time_weighted_median_uA_1uA_bins=median)

def self_test():
    # Algebraic triangle: +100mA to -100mA over two seconds at constant 4V.
    r=test_windows([(0,4,.1,3.3),(2,4,-.1,3.3)],3)
    assert abs(r['battery_discharge_mAh']-.05/3.6)<1e-12 and abs(r['battery_charge_returned_mAh']-.05/3.6)<1e-12
    assert abs(r['battery_net_energy_mWh'])<1e-12
    # Simultaneous V and I ramps have nonzero cross term; known integral 70 J.
    r=test_windows([(0,1,1,0),(30,2,2,0)],30)
    assert abs(r['battery_net_energy_mWh']-70/3.6)<1e-12
    r=test_windows([(0,3.7,20e-6,0),(1,3.7,20e-6,0),(50,3.7,20e-6,0)],60)
    assert r['qualified_sleep_s']==40 and r['sleep_time_weighted_median_uA_1uA_bins']==20
    try: test_windows([(0,3.7,0,0),(3,3.7,0,0)],2)
    except ValueError: pass
    else: raise AssertionError('gap rejection failed')
    print('PASS: synthetic analytic current, energy, sleep and sampling-gap controls. No physical measurement.')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('csv_path',nargs='?',type=Path)
    p.add_argument('--max-gap-s',type=float,default=.01,help='reject longer gaps, default 10 ms; use synchronized high-bandwidth instrument for peaks')
    p.add_argument('--self-test',action='store_true')
    args=p.parse_args()
    if args.self_test:
        self_test();return
    if args.csv_path is None or args.max_gap_s<=0:p.error('supply CSV and a positive gap bound')
    with args.csv_path.open(newline='') as f:
        rows=csv.DictReader(f)
        needed=('time_s','vbat_V','ibat_A','vmain_V')
        if not rows.fieldnames or any(x not in rows.fieldnames for x in needed):p.error('expected '+','.join(needed))
        result=test_windows((tuple(float(row[k]) for k in needed) for row in rows),args.max_gap_s)
    result['source_file']=str(args.csv_path)
    result['sign_convention']='Positive current leaves cell. Recorded peak is limited by instrument bandwidth and sample spacing.'
    json.dump(result,sys.stdout,indent=2);print()

if __name__=='__main__': main()
