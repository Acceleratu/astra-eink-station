// Each pixel indexes a family of colours sampled at the same board position
// in Fusion. A family's palette entry depends only on the layers at that pixel.
const directory = 'explorer/native/';
const crcTable = Uint32Array.from({length: 256}, (_, byte) => {
  let crc = byte;
  for (let bit = 0; bit < 8; bit++) crc = (crc >>> 1) ^ ((crc & 1) ? 0xedb88320 : 0);
  return crc;
});

async function fetchAsset(name) {
  const response = await fetch(directory + name);
  if (!response.ok) throw Error('Could not load ' + name);
  return response;
}

export async function loadLayerImage() {
  const [table, buffer] = await Promise.all([
    fetchAsset('pcb-layer-colors.json').then(response => response.json()),
    fetchAsset('pcb-layer-index.png').then(response => response.arrayBuffer())
  ]);
  const bytes = new Uint8Array(buffer);
  const chunks = new DataView(buffer);
  let offset = 8;
  while (offset + 12 <= bytes.length && chunks.getUint32(offset + 4) !== 0x504c5445) {
    offset += 12 + chunks.getUint32(offset);
  }
  if (offset + 12 > bytes.length) throw Error('Missing PCB palette');
  const size = chunks.getUint32(offset);
  if (size < table.colors.length * 3 || offset + size + 12 > bytes.length) throw Error('Invalid PCB palette');
  const prefix = bytes.subarray(0, offset + 4);
  const suffix = bytes.subarray(offset + 12 + size);
  let lastFlags = -1, url = null;

  function imageFor(enabled) {
    const flags = table.layers.reduce((bits, id, i) => enabled.has(id) ? bits | (1 << i) : bits, 0);
    if (flags === lastFlags) return url;
    // Replace only the PLTE chunk and its checksum. The compressed pixels stay identical.
    const chunk = bytes.slice(offset + 4, offset + 12 + size);
    table.masks.forEach((mask, i) => {
      let index = 0, weight = 1;
      while (mask) {
        const bit = mask & -mask;
        if (flags & bit) index += weight;
        weight *= 2;
        mask ^= bit;
      }
      const rgb = table.colors[i][index], pos = 4 + 3*i;
      chunk[pos] = rgb >>> 16;
      chunk[pos + 1] = rgb >>> 8;
      chunk[pos + 2] = rgb;
    });
    let crc = -1;
    for (const byte of chunk.subarray(0, size + 4)) crc = (crc >>> 8) ^ crcTable[(crc ^ byte) & 255];
    new DataView(chunk.buffer).setUint32(size + 4, ~crc);
    if (url) URL.revokeObjectURL(url);
    url = URL.createObjectURL(new Blob([prefix, chunk, suffix], {type: 'image/png'}));
    lastFlags = flags;
    return url;
  }
  return {imageFor, layers: table.catalog};
}
