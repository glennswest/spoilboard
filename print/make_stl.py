#!/usr/bin/env python3
"""Emit print-ready binary STLs for the flip dogs (no deps).

flip_dog.stl      - two-step ¾″ registration dog (print TWO)
flip_dog_test.stl - 8 mm fit puck, bed diameter only (print FIRST,
                    test in a bed dog hole, adjust BED_D by 0.05)

Same parameters as flip_dog.scad - keep the two in sync.
"""
import math
import struct
import os

BED_D = 19.0     # bed-hole section (hole is 19.05)
PANEL_D = 19.2   # panel-hole section (bore is 19.35)
BED_H = 15.0
PANEL_H = 17.0   # total 32 = 17 stick-up; NEVER exceed 33 total
CH_TOP = 2.0
CH_BOT = 0.5
SEGS = 128

HERE = os.path.dirname(os.path.abspath(__file__))


def solid_of_revolution(profile):
    """profile: list of (r, z) bottom->top, r>0; closed with flat caps."""
    rings = []
    for r, z in profile:
        ring = [(r * math.cos(2 * math.pi * i / SEGS),
                 r * math.sin(2 * math.pi * i / SEGS), z)
                for i in range(SEGS)]
        rings.append(ring)
    tris = []
    # bottom cap (normal -z): fan around centroid
    c0 = (0.0, 0.0, profile[0][1])
    for i in range(SEGS):
        a, b = rings[0][i], rings[0][(i + 1) % SEGS]
        tris.append((c0, b, a))
    # walls
    for k in range(len(rings) - 1):
        lo, hi = rings[k], rings[k + 1]
        for i in range(SEGS):
            j = (i + 1) % SEGS
            tris.append((lo[i], lo[j], hi[j]))
            tris.append((lo[i], hi[j], hi[i]))
    # top cap (+z)
    c1 = (0.0, 0.0, profile[-1][1])
    for i in range(SEGS):
        a, b = rings[-1][i], rings[-1][(i + 1) % SEGS]
        tris.append((c1, a, b))
    return tris


def write_stl(path, tris):
    with open(path, "wb") as f:
        f.write(b"flip_dog" + b" " * 72)
        f.write(struct.pack("<I", len(tris)))
        for a, b, c in tris:
            ux = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
            vx = (c[0] - a[0], c[1] - a[1], c[2] - a[2])
            n = (ux[1] * vx[2] - ux[2] * vx[1],
                 ux[2] * vx[0] - ux[0] * vx[2],
                 ux[0] * vx[1] - ux[1] * vx[0])
            ln = math.sqrt(n[0] ** 2 + n[1] ** 2 + n[2] ** 2) or 1.0
            f.write(struct.pack("<3f", n[0] / ln, n[1] / ln, n[2] / ln))
            for p in (a, b, c):
                f.write(struct.pack("<3f", *p))
            f.write(struct.pack("<H", 0))
    print(f"wrote {path} ({len(tris)} tris)")


def main():
    dog = [
        (BED_D / 2 - CH_BOT, 0.0),
        (BED_D / 2, CH_BOT),
        (BED_D / 2, BED_H),
        (PANEL_D / 2, BED_H),
        (PANEL_D / 2, BED_H + PANEL_H - CH_TOP),
        (PANEL_D / 2 - CH_TOP, BED_H + PANEL_H),
    ]
    write_stl(os.path.join(HERE, "flip_dog.stl"), solid_of_revolution(dog))

    puck = [
        (BED_D / 2 - CH_BOT, 0.0),
        (BED_D / 2, CH_BOT),
        (BED_D / 2, 7.0),
        (BED_D / 2 - 1.0, 8.0),
    ]
    write_stl(os.path.join(HERE, "flip_dog_test.stl"),
              solid_of_revolution(puck))


if __name__ == "__main__":
    main()
