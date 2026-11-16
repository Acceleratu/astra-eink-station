#!/usr/bin/env python3
"""Reconcile the design BOM against JLCPCB's live public PCBA library."""
import argparse
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import csv
from datetime import datetime, timezone
import gzip
import hashlib
import json
import math
from pathlib import Path
import re
import time
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DETAIL = 'https://cart.jlcpcb.com/shoppingCart/smtGood/getComponentDetail?componentCode='
SEARCH = 'https://jlcpcb.com/api/overseas-pcb-order/v1/shoppingCart/smtGood/selectSmtComponentList'
MODULES = ('power', 'radio', 'display', 'wake')


def get_json(request):
    for attempt in range(3):
        try:
            with urlopen(request, timeout=25) as response:
                raw = response.read()
                obj = json.loads(raw)
                if str(obj.get('code')) != '200' or not obj.get('data'):
                    raise ValueError(f"No catalog data: {obj.get('message')}")
                return obj['data'], raw
        except (OSError, ValueError):
            if attempt == 2:
                raise
            time.sleep(1 + attempt)


def find(query):
    payload = json.dumps({'keyword': query, 'page': 1, 'pageSize': 100}).encode()
    req = Request(SEARCH, payload, headers={
        'Content-Type': 'application/json', 'Referer': 'https://jlcpcb.com/parts', 'User-Agent': 'Mozilla/5.0'})
    body, raw = get_json(req)
    return body['componentPageInfo']['list'], raw


def catalogue(code, out):
    result = {'retrieved_utc': datetime.now(timezone.utc).isoformat(), 'detail_url': DETAIL + code}
    try:
        data, raw = get_json(Request(DETAIL + code, headers={'User-Agent': 'Mozilla/5.0'}))
        if data['componentCode'] != code:
            raise ValueError('Wrong part returned by catalog')
        (out / f'{code}.json.gz').write_bytes(gzip.compress(raw, mtime=0))
        result.update({k: data.get(k) for k in ('componentCode', 'componentModelEn', 'componentBrandEn',
            'componentSpecificationEn', 'assemblyProcess', 'componentLibraryType', 'componentStatus',
            'stockCount', 'overseasStockCount', 'canPresaleNumber', 'leastPatchNumber', 'lossNumber',
            'largeUsageLossRatio', 'xrayFlag', 'dataManualOfficialLink', 'dataManualUrl')})
        result['response_sha256'] = hashlib.sha256(raw).hexdigest()
    except (ValueError, KeyError, OSError) as err:
        result['error'] = str(err)
    return code, result


def check(rows, out, count):
    out.mkdir(exist_ok=True, parents=True)
    parts = defaultdict(list)
    for part in rows:
        parts[(str(part.get('lcsc') or '').strip().upper(), str(part.get('mpn') or '').strip())].append(part['ref'])
    codes = sorted({code for code, _ in parts if re.fullmatch(r'C\d+', code)})
    with ThreadPoolExecutor(max_workers=5) as workers:
        details = dict(workers.map(lambda c: catalogue(c, out), codes))
    for cached in out.glob('C*.json.gz'):
        if re.fullmatch(r'C\d+\.json\.gz', cached.name) and cached.name.split('.')[0] not in codes:
            cached.unlink()
    (out / 'details.json').write_text(json.dumps(details, indent=2) + '\n')
    with (out / 'availability.csv').open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(('Reference(s)', 'Design MPN', 'JLCPCB part', 'Official MPN', 'Brand', 'Package',
            'PCBA type', 'Assembly process', 'Stock', 'Available order quantity (parts library)', 'Sample build quantity', 'Parts required',
            'Min placement quantity (catalog)', 'Attrition quantity (catalog)', 'Large-usage loss ratio (catalog)', 'Conservative feed quantity',
            'Assessment', 'Retrieved UTC', 'Evidence URL', 'Response SHA256'))
        for (code, mpn), refs in sorted(parts.items()):
            entry = details.get(code, {})
            needed = len(refs) * count
            qty = entry.get('canPresaleNumber')
            stock = entry.get('stockCount')
            floor,loss,fraction=[entry.get(key) for key in ('leastPatchNumber','lossNumber','largeUsageLossRatio')]
            feed=max(floor,needed+max(loss,math.ceil(needed*fraction))) if all(isinstance(x,(float,int)) for x in (floor,loss,fraction)) else None
            if not entry:
                outcome = 'Missing manufacturer catalog code'
            elif entry.get('error'):
                outcome = 'Catalog read error'
            elif mpn.upper() != str(entry['componentModelEn']).upper():
                outcome = 'MPN mismatch'
            elif entry.get('componentStatus') != 'yes' or not isinstance(qty, (float, int)) or not isinstance(stock, (float, int)) or feed is None:
                outcome = 'Unknown status / inventory'
            elif stock < feed:
                outcome = 'Insufficient on-hand inventory for sample and feeder minimum/attrition'
            elif qty < feed:
                outcome = 'Stock covers sample and feed allowance; parts-library pre-purchase quantity below allowance'
            else:
                outcome = 'Stock and parts-library pre-purchase quantity cover sample and feed allowance'
            writer.writerow([','.join(sorted(refs)), mpn, code, entry.get('componentModelEn'), entry.get('componentBrandEn'),
                entry.get('componentSpecificationEn'), entry.get('componentLibraryType'), entry.get('assemblyProcess'), stock,
                qty, count, needed, floor,loss,fraction,feed,outcome, entry.get('retrieved_utc'), entry.get('detail_url'), entry.get('response_sha256')])
    return details


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--search', metavar='MPN')
    parser.add_argument('--probe', nargs='*', metavar='MPN@C_CODE')
    parser.add_argument('--output', type=Path, default=ROOT / 'verification/manufacturing/stock')
    parser.add_argument('--quantity', type=int, default=2)
    args = parser.parse_args()
    if args.search:
        rows, raw = find(args.search)
        for p in rows:
            print(p['componentModelEn'], p['componentCode'], p.get('componentSpecificationEn'),
                  p.get('stockCount'), p.get('canPresaleNumber'))
        return
    if args.probe:
        rows = [{'mpn': s.split('@')[0], 'lcsc': s.split('@')[1], 'ref': s.split('@')[0]} for s in args.probe]
    else:
        rows = []
        for mod in MODULES:
            parts = json.loads((ROOT / f'hardware/{mod}.json').read_text())['parts']
            rows.extend(p for p in parts if populated(p))
    check(rows, args.output, args.quantity)


def populated(part):
    if part.get('dnp') or part.get('populate') is False or part.get('populated') is False:
        return False
    if str(part.get('assembly', '')).upper() in {'DNP', 'PCB', 'PCB-ONLY', 'CUSTOMER', 'EXTERNAL'}:
        return False
    if part['footprint'] == 'TP' or re.match(r'^(TP|FID|MH)\d+$', part['ref']):
        return False
    return True


if __name__ == '__main__':
    main()
