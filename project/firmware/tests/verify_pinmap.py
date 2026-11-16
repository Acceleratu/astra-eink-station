#!/usr/bin/env python3
"""Cross-check compiled, resolved Zephyr DT with Fusion XML library-to-pad mappings."""
import argparse
import csv
from hashlib import sha256
import os
from pathlib import Path
import sys
from xml.etree import ElementTree as ET

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--board', type=Path, help='also compare contactrefs in final Fusion board XML')
    ap.add_argument('--expect-board-sha256', help='require the exact released board SHA-256')
    ap.add_argument('--expect-schematic-sha256', help='require the exact released schematic SHA-256')
    ns = ap.parse_args()
    if ns.expect_board_sha256 and not ns.board:
        ap.error('--expect-board-sha256 requires --board')
    root = Path(__file__).resolve().parents[2]
    checked_files = [root/'schematic/astra.sch', root/'firmware/artifacts/resolved.dts',
                     root/'firmware/artifacts/astra.hex', root/'verification/radio/mcu-crosswalk.csv']
    if ns.board:
        checked_files.append(ns.board.resolve())
    def hashes():
        return {path:sha256(path.read_bytes()).hexdigest() for path in checked_files}
    original=hashes()
    if ns.expect_schematic_sha256:
        assert original[root/'schematic/astra.sch']==ns.expect_schematic_sha256, 'schematic SHA-256 mismatch'
    if ns.expect_board_sha256:
        assert original[ns.board.resolve()]==ns.expect_board_sha256, 'board SHA-256 mismatch'
    sys.path.insert(0, str(Path(os.environ['ZEPHYR_BASE']) / 'scripts/dts/python-devicetree/src'))
    from devicetree import dtlib
    dt = dtlib.DT(str(root / 'firmware/artifacts/resolved.dts'))
    user = dt.get_node('/zephyr,user')
    gpio = {}
    def pin(name,node,prop,index=0,want_active_low=False):
        cells = dtlib.to_nums(node.props[prop].value)
        phandle, bit, flags = cells[3*index:3*index+3]
        port = dt.phandle2node[phandle].props['port'].to_num()
        assert bool(flags & 1)==want_active_low
        gpio[name]=f'P{port}.{bit:02d}'
    pin('TIMER_DONE',user,'done-gpios')
    pin('VBAT_MEAS_EN',user,'measure-enable-gpios')
    for i in range(3):
        pin(f'BTN{i+1}',user,'button-gpios',i)
    pin('EPD_CS',dt.label2node['spi00'],'cs-gpios',want_active_low=True)
    pin('EPD_RST',user,'epd-reset-gpios',want_active_low=True)
    pin('EPD_BUSY',user,'epd-busy-gpios')
    pin('EPD_DC',user,'epd-dc-gpios')
    for peripheral,functions in [('spi00',{4:'EPD_SCK',5:'EPD_MOSI'}),('i2c21',{11:'SCL',12:'SDA'})]:
        state=dt.label2node[peripheral].props['pinctrl-0'].to_nodes()[0]
        for sel in state.nodes['group1'].props['psels'].to_nums():
            gpio[functions[sel>>24]]=f'P{(sel & 0x1ff)//32}.{(sel & 31):02d}'
    ch=dt.label2node['adc'].nodes['channel@0']
    # Zephyr v4.3.0 adc_nrfx_saadc.c explicitly maps nRF54L15 AIN0 (binding value 1) to P1.04.
    assert ch.props['zephyr,input-positive'].to_num()==1 and ch.props['zephyr,resolution'].to_num()==12
    gpio['VBAT_SENSE']='P1.04'
    assert dt.label2node['bme'].props['reg'].to_num()==0x76
    assert dt.label2node['external_rtc'].props['reg'].to_num()==0x51
    assert dt.label2node['panel'].props['spi-max-frequency'].to_num()==2_000_000
    assert dt.label2node['panel'].props['spi-cs-setup-delay-ns'].to_num()==1000
    assert dt.label2node['panel'].props['spi-cs-hold-delay-ns'].to_num()==1000
    assert dt.label2node['i2c21'].props['clock-frequency'].to_num()==100_000
    assert dt.label2node['hfxo'].props['load-capacitance-femtofarad'].to_num()==15000
    assert dt.label2node['lfxo'].props['load-capacitance-femtofarad'].to_num()==17000
    rows = list(csv.DictReader((root/'verification/radio/mcu-crosswalk.csv').open()))
    crosswalk={r['carrier net']:r for r in rows}
    assert set(gpio)=={n for n,r in crosswalk.items() if r['MCU pin function'].startswith('P')}
    source=ET.parse(root/'schematic/astra.sch').find('.//schematic')
    part=source.find("./parts/part[@name='U201']")
    lib=source.find(f"./libraries/library[@name='{part.get('library')}']")
    dev=lib.find(f"./devicesets/deviceset[@name='{part.get('deviceset')}']/devices/device[@name='{part.get('device')}']")
    pads={(c.get('gate'),c.get('pin')):c.get('pad') for c in dev.findall('connects/connect')}
    physical={}
    for net in source.findall('sheets/sheet/nets/net'):
        for ref in net.findall(".//pinref[@part='U201']"):
            physical.setdefault(net.get('name'),set()).add(pads[ref.get('gate'),ref.get('pin')])
    # Also verify the opposite ends of each digital interface through the Fusion library.
    def contacts(ref):
        part=source.find(f"./parts/part[@name='{ref}']")
        library=source.find(f"./libraries/library[@name='{part.get('library')}']")
        device=library.find(f"./devicesets/deviceset[@name='{part.get('deviceset')}']/devices/device[@name='{part.get('device')}']")
        land={ (c.get('gate'),c.get('pin')):c.get('pad') for c in device.findall('connects/connect') }
        return {land[p.get('gate'),p.get('pin')]:net.get('name')
                for net in source.findall('sheets/sheet/nets/net')
                for p in net.findall(f".//pinref[@part='{ref}']")}
    far_ends={
        'J301':{'8':'GND','9':'EPD_BUSY','10':'EPD_RST','11':'EPD_DC','12':'EPD_CS','13':'EPD_SCK','14':'EPD_MOSI','15':'VMAIN','16':'VMAIN'},
        'U403':{'1':'RTC_XI','2':'RTC_XO','3':'RTC_IRQ_N','4':'GND','5':'SDA','6':'SCL','8':'VAON'},
        'U404':{'1':'GND','2':'VMAIN','3':'SDA','4':'SCL','5':'GND','6':'VMAIN','7':'GND','8':'VMAIN'},
        'J201':{'1':'GND','2':'VMAIN','3':'SWCLK','4':'SWDIO','5':'NRST','6':'WAKE_MDRV','7':'VAON'},
    }
    for ref, expected in far_ends.items():
        actual=contacts(ref)
        for pad,net in expected.items(): assert actual.get(pad)==net,(ref,pad,net,actual.get(pad))
    board={}
    if ns.board:
        board_contacts = {ref:{} for ref in far_ends}
        for net in ET.parse(ns.board).findall('.//board/signals/signal'):
            board[net.get('name')]={ref.get('pad') for ref in net.findall("contactref[@element='U201']")}
            for c in net.findall('contactref'):
                ref, pad = c.get('element'), c.get('pad')
                if ref in far_ends and pad in far_ends[ref]:
                    assert pad not in board_contacts[ref], (ref,pad,'duplicate contactref')
                    board_contacts[ref][pad]=net.get('name')
        assert board_contacts==far_ends, 'opposite-end contactrefs absent or on different nets' 
    for net,func in sorted(gpio.items()):
        row=crosswalk[net]; pad=row['module pad']
        assert row['MCU pin function']==func,(net,func,row)
        assert physical[net]=={pad},(net,physical.get(net),pad)
        if ns.board: assert board[net]=={pad},(net,board.get(net),pad)
        print(f'{net:16} {func:6} U201.{pad:2}  QFN48.{row["QFN48 physical pin"]}')
    for net in ('SWCLK','SWDIO','NRST'):
        assert physical[net]=={crosswalk[net]['module pad']}
        if ns.board: assert board[net]==physical[net]
    print('PASS 14 firmware signals and 3 SWD/reset lands against supplier crosswalk and Fusion schematic')
    if ns.board: print(f'PASS all 17 against Fusion board contactrefs in {ns.board.name}')
    print(f'PASS {sum(len(pads) for pads in far_ends.values())} opposite-end lands on J301 display, U403 RTC, U404 sensor and J201 pogo fixture')
    print('PASS ADC AIN0, BME=0x76, RTC=0x51, I2C 100 kHz, SPI 2 MHz, 1 us CS setup/hold and HF/LF load settings')

    assert hashes()==original, 'inputs changed during the comparison'
    print('\nSHA-256 of unchanged inputs before and after verification')
    for path,digest in original.items():
        name=path.relative_to(root) if path.is_relative_to(root) else path
        print(f'{digest}  {name}')

if __name__=='__main__': main()
