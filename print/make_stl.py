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

BED_D = 19.1     # bed-hole section (hole is 19.05; +0.1 fit comp, puck was loose)
PANEL_D = 19.3   # panel-hole section (bore is 19.35; same +0.1 comp)
BED_H = 15.0
PANEL_H = 17.0   # total 32 = 17 stick-up; NEVER exceed 33 total
CH_TOP = 2.0
CH_BOT = 0.5
SEGS = 128

# FENCE PINS (owner: shelf d8 pins too loose): fit the d8 x 10
# blind fence holes. Bottom section = snug hole fit (tune);
# upper section = the DATUM the panel edge bears on - keep it
# 8.00 nominal (holes are tangent to the zero lines, so a fatter
# pin shifts the fence line by half the oversize).
FP_BED_D = 9.15     # hole-fit section (owner: 8.15 still loose
                    # fully seated - holes are well over nominal)
FP_DATUM_D = 8.00   # bearing section - the fence datum. Mic the
                    # printed datum; if it mics under 8.00, add the
                    # shortfall here (as-printed datum must BE 8.00).
FP_BED_H = 10.0     # hole depth
FP_UP_H = 15.0      # stick-up (panel 12-13 + margin)
FP_CH = 1.2

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

    pin = [
        (FP_BED_D / 2 - CH_BOT, 0.0),
        (FP_BED_D / 2, CH_BOT),
        (FP_BED_D / 2, FP_BED_H),
        (FP_DATUM_D / 2, FP_BED_H),
        (FP_DATUM_D / 2, FP_BED_H + FP_UP_H - FP_CH),
        (FP_DATUM_D / 2 - FP_CH, FP_BED_H + FP_UP_H),
    ]
    write_stl(os.path.join(HERE, "fence_pin.stl"),
              solid_of_revolution(pin))

    fpuck = [
        (FP_BED_D / 2 - CH_BOT, 0.0),
        (FP_BED_D / 2, CH_BOT),
        (FP_BED_D / 2, 6.0),
        (FP_BED_D / 2 - 1.0, 7.0),
    ]
    write_stl(os.path.join(HERE, "fence_pin_test.stl"),
              solid_of_revolution(fpuck))

    puck = [
        (BED_D / 2 - CH_BOT, 0.0),
        (BED_D / 2, CH_BOT),
        (BED_D / 2, 7.0),
        (BED_D / 2 - 1.0, 8.0),
    ]
    write_stl(os.path.join(HERE, "flip_dog_test.stl"),
              solid_of_revolution(puck))

    # PLUG GAUGES - stepped pucks that MEASURE the holes (no
    # calipers needed): push in gently until it stops; the first
    # band still showing above the surface = the hole is SMALLER
    # than that band's diameter (and bigger than the band below).
    # Bands small->big going up; each is labeled in the knob note
    # printed below. Print one of each, flat side down, as modeled.
    def gauge(name, bands, band_h, knob_d):
        prof = [(bands[0] / 2 - CH_BOT, 0.0), (bands[0] / 2, CH_BOT)]
        z = 0.0
        for i, d in enumerate(bands):
            if i:
                prof.append((d / 2, z))
            z += band_h
            prof.append((d / 2, z))
        prof += [(knob_d / 2, z), (knob_d / 2, z + 6.0),
                 (knob_d / 2 - 1.0, z + 7.0)]
        write_stl(os.path.join(HERE, name), solid_of_revolution(prof))
        steps = " / ".join(f"{d:.2f}" for d in bands)
        print(f"  {name}: bands bottom->top {steps} x {band_h} tall")

    # fence holes are 10 deep: 5 x 2 mm bands cover 8.2-9.0
    gauge("fence_gauge.stl", [8.2, 8.4, 8.6, 8.8, 9.0], 2.0, 14.0)
    # dog holes are 15 deep: 5 x 3 mm bands cover 19.1-19.5
    gauge("dog_gauge.stl", [19.1, 19.2, 19.3, 19.4, 19.5], 3.0, 26.0)


if __name__ == "__main__":
    main()
