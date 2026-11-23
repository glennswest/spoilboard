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

BED_CORE_D = 19.05  # crush-rib bed fit: core...
BED_RIB = 0.35      # ...plus 8 ribs this proud (OD 19.75): fits
                    # any hole 19.15-19.75, shaves to size (same
                    # proven design as the fence pin, v0.7.0)
PANEL_D = 19.3   # panel-hole section PLAIN (bore is 19.35): the
                 # panel must DROP onto two dogs at once in the
                 # flip, so this one keeps slight clearance
BED_H = 15.0
PANEL_H = 17.0   # total 32 = 17 stick-up; NEVER exceed 33 total
                 # (full height kept: the crate long run JUMPS its
                 # rapids over the dogs - crate v0.18.1+)
CH_TOP = 2.0
CH_BOT = 0.5
SEGS = 128

# FENCE PINS (owner: shelf d8 pins too loose): fit the d8 x 10
# blind fence holes. Bottom section = snug hole fit (tune);
# upper section = the DATUM the panel edge bears on - keep it
# 8.00 nominal (holes are tangent to the zero lines, so a fatter
# pin shifts the fence line by half the oversize).
FP_CORE_D = 8.0     # crush-rib fit: core diameter...
FP_RIB = 0.35       # ...plus 6 ribs this proud (OD 8.7). Fits any
                    # hole 8.1-8.7: ribs shave to size, self-center.
                    # (The "loose 9.15" scare was a stale slicer
                    # mesh - the 3mf still held the 8.15 pin. Holes
                    # are ~8.3-8.5 after three machining passes.)
FP_DATUM_D = 8.00   # bearing section - the fence datum. Mic the
                    # printed datum; if it mics under 8.00, add the
                    # shortfall here (as-printed datum must BE 8.00).
FP_BED_H = 10.0     # hole depth
FP_UP_H = 15.0      # stick-up (panel 12-13 + margin)
FP_CH = 1.2

HERE = os.path.dirname(os.path.abspath(__file__))


def loft(rings):
    """rings: list of same-length [(x,y,z)] loops bottom->top;
    closed with flat caps (same triangle pattern as the revolve)."""
    tris = []
    n = len(rings[0])
    c0 = (0.0, 0.0, rings[0][0][2])
    for i in range(n):
        a, b = rings[0][i], rings[0][(i + 1) % n]
        tris.append((c0, b, a))
    for k in range(len(rings) - 1):
        lo, hi = rings[k], rings[k + 1]
        for i in range(n):
            j = (i + 1) % n
            tris.append((lo[i], lo[j], hi[j]))
            tris.append((lo[i], hi[j], hi[i]))
    c1 = (0.0, 0.0, rings[-1][0][2])
    for i in range(n):
        a, b = rings[-1][i], rings[-1][(i + 1) % n]
        tris.append((c1, a, b))
    return tris


def ribbed_ring(z, core_r, rib_h, scale=1.0, ribs=6, half_deg=8.0):
    """Circle of core_r with `ribs` raised pads rib_h proud."""
    pts = []
    for i in range(SEGS):
        th = 2 * math.pi * i / SEGS
        deg = math.degrees(th) % (360.0 / ribs)
        r = core_r + (rib_h if min(deg, 360.0 / ribs - deg) <= half_deg
                      else 0.0)
        r *= scale
        pts.append((r * math.cos(th), r * math.sin(th), z))
    return pts


def circle_ring(z, r):
    return [(r * math.cos(2 * math.pi * i / SEGS),
             r * math.sin(2 * math.pi * i / SEGS), z)
            for i in range(SEGS)]


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
    bc, bh = BED_CORE_D / 2.0, BED_RIB
    dog_rings = [
        ribbed_ring(0.0, bc, bh, scale=0.95, ribs=8),   # lead-in
        ribbed_ring(1.5, bc, bh, ribs=8),
        ribbed_ring(BED_H, bc, bh, ribs=8),             # ribbed bed
        circle_ring(BED_H, PANEL_D / 2),                # plain panel
        circle_ring(BED_H + PANEL_H - CH_TOP, PANEL_D / 2),
        circle_ring(BED_H + PANEL_H, PANEL_D / 2 - CH_TOP),
    ]
    write_stl(os.path.join(HERE, "flip_dog.stl"), loft(dog_rings))

    cr, rh = FP_CORE_D / 2.0, FP_RIB
    pin_rings = [
        ribbed_ring(0.0, cr, rh, scale=0.92),        # lead-in taper
        ribbed_ring(1.5, cr, rh),
        ribbed_ring(FP_BED_H, cr, rh),               # ribbed fit, 10 deep
        circle_ring(FP_BED_H, FP_DATUM_D / 2.0),     # step to datum
        circle_ring(FP_BED_H + FP_UP_H - FP_CH, FP_DATUM_D / 2.0),
        circle_ring(FP_BED_H + FP_UP_H, FP_DATUM_D / 2.0 - FP_CH),
    ]
    write_stl(os.path.join(HERE, "fence_pin.stl"), loft(pin_rings))

    fpuck_rings = [
        ribbed_ring(0.0, cr, rh, scale=0.92),
        ribbed_ring(1.5, cr, rh),
        ribbed_ring(6.0, cr, rh),
        ribbed_ring(7.0, cr, rh, scale=0.9),
    ]
    write_stl(os.path.join(HERE, "fence_pin_test.stl"), loft(fpuck_rings))

    puck_rings = [
        ribbed_ring(0.0, bc, bh, scale=0.95, ribs=8),
        ribbed_ring(1.5, bc, bh, ribs=8),
        ribbed_ring(7.0, bc, bh, ribs=8),
        ribbed_ring(8.0, bc, bh, scale=0.92, ribs=8),
    ]
    write_stl(os.path.join(HERE, "flip_dog_test.stl"), loft(puck_rings))

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
