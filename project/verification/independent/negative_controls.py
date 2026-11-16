#!/usr/bin/env python3
"""Introduce known errors into *temporary* fixtures. Never modifies native design."""
from copy import deepcopy
from pathlib import Path
import json
from tempfile import TemporaryDirectory
from xml.etree import ElementTree as ET
from review_design import ROOT, board_pads, schematic_pads, audit_pads, corners, native_stack

def main():
    doc=ET.parse(ROOT/'schematic/astra.sch')
    # Flip red/black physical-number connects in the indicated part's deviceset.
    cell=doc.find(".//schematic/parts/part[@name='J102']")
    assert cell is not None
    lib=doc.find(f".//schematic/libraries/library[@name='{cell.get('library')}']")
    ds=lib.find(f"devicesets/deviceset[@name='{cell.get('deviceset')}']")
    con=ds.find('devices/device/connects')
    a,b=[con.find(f"connect[@pad='{i}']") for i in ('1','3')]
    assert a is not None and b is not None
    a.set('pad','3');b.set('pad','1')
    with TemporaryDirectory() as t:
        mut=Path(t)/'reversed.sch';doc.write(mut)
        e=audit_pads(*schematic_pads(mut))['errors']
    assert any('J102.1' in x for x in e) and any('J102.3' in x for x in e)
    parts={p['ref']:p for f in ('power','wake') for p in json.loads((ROOT/f'hardware/{f}.json').read_text())['parts']}
    bad=deepcopy(parts)
    for k,v in [('R108','5.1M'),('R109','1.1M'),('R110','2M')]: bad[k]['value']=v+' 1%'
    c=corners(bad)['checks']
    assert c['SPV output ladder 10 to 20 MΩ inclusive'] is False
    bad=deepcopy(parts);bad['R119']['value']='47k 1%'
    c=corners(bad)['checks']
    assert c['NTC guard band, at stated error bounds, stays inside pack 10..45°C'] is False
    board=ET.parse(ROOT/'board/astra.brd').find('.//board')
    board.find("elements/element[@name='U201']").set('rot','MR270')
    board.find('signals/signal/wire').set('layer','2')
    stack=native_stack(board)
    assert stack['mirrored_elements']==['U201'] and stack['routed_layer_uses']['wire']['2']==1
    assert sum(not passed for passed in stack['checks'].values())==2
    owned,mapped=board_pads(ROOT/'board/astra.brd')
    for pad,net in [('1','PV_IN'),('2','PV_IC_IN')]:
        owned.add(('BYPASS',pad)); mapped['BYPASS',pad]=net
    e=audit_pads(owned,mapped)['errors']
    assert len(e)==2 and all('R126 series measurement' in error for error in e)
    print('PASS: reversed J102, invalid SPV ladder sum, unsafe NTC window, mirrored MCU, inner-layer trace and simulated bypass of R126 were all detected (temporary fixtures).')

if __name__=='__main__': main()
