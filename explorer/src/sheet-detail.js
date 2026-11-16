// Keep the lightweight overview at fit. At reading scale, place the visible
// high-resolution tiles in the same drawing coordinates as the native frame.
export function updateSheetDetail(svg, detail) {
  if (!detail || !svg.isConnected) return;
  const matrix = svg.getScreenCTM();
  if (!matrix || !matrix.a) return;
  const {group, sheet, number, tileSize, previewWidth} = detail;
  const [x, y, width, height] = sheet.box;
  const [pixelsX, pixelsY] = sheet.size;
  if (matrix.a * window.devicePixelRatio < previewWidth / width * .78) {
    group.replaceChildren();
    return;
  }
  const rect = svg.getBoundingClientRect();
  const inverse = matrix.inverse();
  const start = new DOMPoint(rect.left, rect.top).matrixTransform(inverse);
  const end = new DOMPoint(rect.right, rect.bottom).matrixTransform(inverse);
  const stepX = width / pixelsX, stepY = height / pixelsY;
  const minCol = Math.max(0, Math.floor((start.x - x) / (stepX * tileSize)));
  const maxCol = Math.min(Math.ceil(pixelsX / tileSize)-1, Math.floor((end.x - x) / (stepX * tileSize)));
  const minRow = Math.max(0, Math.floor((start.y - y) / (stepY * tileSize)));
  const maxRow = Math.min(Math.ceil(pixelsY / tileSize)-1, Math.floor((end.y - y) / (stepY * tileSize)));
  const old = new Map(Array.from(group.children, node => [node.dataset.tile, node]));
  for (let row = minRow; row <= maxRow; row++) {
    for (let col = minCol; col <= maxCol; col++) {
      const key = number + '-' + col + '-' + row;
      if (old.delete(key)) continue;
      const left = Math.max(0, col * tileSize - 2), top = Math.max(0, row * tileSize - 2);
      const right = Math.min(pixelsX, (col + 1) * tileSize + 2);
      const bottom = Math.min(pixelsY, (row + 1) * tileSize + 2);
      const tile = document.createElementNS(svg.namespaceURI, 'image');
      tile.dataset.tile = key;
      tile.setAttribute('x', x + left * stepX);
      tile.setAttribute('y', y + top * stepY);
      tile.setAttribute('width', (right - left) * stepX);
      tile.setAttribute('height', (bottom - top) * stepY);
      tile.setAttribute('preserveAspectRatio', 'none');
      tile.setAttribute('href', 'explorer/native/schematic/' + key + '.webp');
      group.append(tile);
    }
  }
  for (const stale of old.values()) stale.remove();
}
