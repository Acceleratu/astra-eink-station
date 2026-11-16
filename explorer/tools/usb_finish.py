"""Register isolated orthographic Fusion captures to the USB connector and housing meshes.

Each source image is a square viewport centered on (-3.2, 67, 1.725) mm in the
assembled coordinates of the isolated part. RGB stores the native appearance.
Alpha stores the distance to the visible CAD surface along the camera axis.
"""
import argparse
import json
import struct
from pathlib import Path

import numpy as np
from PIL import Image

VIEWS = {'05-usb': (-1, .20, .22), '10-usb-axial': (-1, 0, 0),
         '11-usb-opposite': (-1, -.32, -.34)}
TARGET = np.array([-3.2, 67, 1.725])


def mesh(path, name):
    raw = path.read_bytes()
    length = struct.unpack_from('<I', raw, 12)[0]
    doc = json.loads(raw[20:20 + length])
    binary = memoryview(raw)[28 + length:]
    node = next(n for n in doc['nodes'] if n['name'] == name)
    primitive, = doc['meshes'][node['mesh']]['primitives']

    def array(index):
        a = doc['accessors'][index]
        v = doc['bufferViews'][a['bufferView']]
        dtype = {5123: '<u2', 5125: '<u4', 5126: '<f4'}[a['componentType']]
        return np.frombuffer(binary[v['byteOffset']:v['byteOffset'] + v['byteLength']], dtype)

    return array(primitive['attributes']['POSITION']).reshape(-1, 3), array(primitive['indices']).reshape(-1, 3)


def depth_image(points, triangles, direction, extent, size):
    normal = direction / np.linalg.norm(direction)
    right = np.cross([0, -1, 0], normal)
    right /= np.linalg.norm(right)
    up = np.cross(normal, right)
    relative = points - TARGET
    screen = (relative @ np.stack((right, -up)).T / extent + .5) * size - .5
    height = relative @ normal
    depth = np.full((size, size), -np.inf)
    corners = screen[triangles]
    low = np.maximum(0, np.ceil(corners.min(axis=1)).astype(int))
    high = np.minimum(size - 1, np.floor(corners.max(axis=1)).astype(int))
    for idx in np.flatnonzero(np.all(low <= high, axis=1)):
        (x0, y0), (x1, y1) = low[idx], high[idx]
        a, b, c = corners[idx]
        u, v = b - a, c - a
        det = u[0]*v[1] - v[0]*u[1]
        if abs(det) < 1e-9:
            continue
        yy, xx = np.ogrid[y0:y1+1, x0:x1+1]
        tx, ty = xx - a[0], yy - a[1]
        w1 = (tx*v[1] - ty*v[0]) / det
        w2 = (u[0]*ty - u[1]*tx) / det
        z = height[triangles[idx]]
        section = depth[y0:y1+1, x0:x1+1]
        np.maximum(section, z[0]+w1*(z[1]-z[0])+w2*(z[2]-z[0]), out=section,
                   where=(w1 >= 0) & (w2 >= 0) & (w1+w2 <= 1))
    valid = (depth >= -16) & (depth <= 16)
    alpha = np.zeros(depth.shape, dtype=np.uint8)
    alpha[valid] = 1 + np.rint((depth[valid]+16)*7.8).astype(np.uint8)
    return alpha


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('captures', type=Path)
    ap.add_argument('explorer', type=Path)
    args = ap.parse_args()
    for prefix, model, name, extent in [('finish', 'pcb', 'J101', 14), ('shell', 'enclosure', 'front_shell', 28)]:
        points, triangles = mesh(args.explorer/'data'/f'{model}.glb', name)
        for key, direction in VIEWS.items():
            image = Image.open(args.captures/f'{prefix}-{key}.png').convert('RGBA')
            assert image.width == image.height
            alpha = depth_image(points, triangles, direction, extent, image.width)
            alpha[np.asarray(image.getchannel('A')) < 250] = 0
            image.putalpha(Image.fromarray(alpha))
            image.save(args.explorer/'native'/f'{prefix}-{key}.webp', lossless=True, method=4)


if __name__ == '__main__':
    main()
