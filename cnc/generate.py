#!/usr/bin/env python3
"""spoilboard - Onefinity Foreman Elite (Masso G3) machine + QCW
spoilboard setup cut files.

Everything that belongs to the MACHINE rather than to any furniture
project: work-zero programming, leveling (skim) jobs, toolsetter bit
changes, track measurement, and the slat workholding grid. Extracted
from glennswest/thetable v0.51.0 (owner 2026-11-13: each project its
own repo + its own numbered folder on the MASSO stick).

Output files are STICK-READY: numbered from 00, copy them into the
stick's /spoilboard folder (cnc/stick.py does it).

  00_set_work_zero      program G54 XY0 (machine 18.184, 68.584)
  01_level_test         dry-run of the leveling extents, spindle off
  02_toolchange_surfacing  M6 -> T2 (1in surfacing) via toolsetter
  03_level              skim pass 1 (-0.5), full machine reach
  04_level_deep         follow-on passes 2..3 - SAME Z0, no re-touch
  05_level_edges        side strips, full 3-depth ladder
  06_toolchange_quarter M6 -> T1 (1/4in) via toolsetter
  07_track_targets      parks over the 4 slot centers (M00 pauses)
  08_pins               fence pins + dog holes + M6 insert bores
  09_insert_guide       driver jig for the M6x13 inserts (cut x2)

Conventions (same as thetable): MASSO ISO dialect, Z0 = stock /
spoilboard top, SAFE START (G53 Z0 -> XY -> only then Z down), every
file ends parked at machine (610, 30) full height - mid X, front,
spindle in reach. All dimensions mm. Pure Python 3, no deps.
"""
import math
import os

VERSION = "0.1.0"

PARAMS = {
    # MACHINE (measured on the owner's Foreman Elite, 2026-11-11/12)
    "cnc": {
        "bed": 1155.0,               # sheet window (nest zone)
        "origin": (18.184, 68.584),  # G54 XY0 in machine coords
        "inset": 15.0,               # XY0 = slat corner + this
        "travel": (1219.998, 1228.718),
        "park": (610.0, 30.0),       # end-of-file park (machine, Z top)
        # G54 Z reference 2026-11-12 (Masso F4 displays INCHES:
        # -0.53740in): slat top = machine Z -13.650 after the -1.5
        # skim. REFERENCE ONLY - re-touch after any re-skim.
        "g54_z": -13.650,
    },
    # QCW slat tracks - ref measured 2026-11-12 via track_targets:
    # all 4 parks were dead center read as MACHINE X -> true work
    # centers = manual-p20 prediction minus origin X. Slot 1 anchors.
    "tracks": {"ref": (1, 227.871), "verify": None,
               "lines": [], "outer_w": None, "span": None,
               "track_gap": 20.46,
               "pitch": 0.0, "offset": 0.0, "dir": "y",
               "guard": 20.0, "grid": 101.6,
               "dog_d": 19.05, "dog_depth": 15.0,
               "insert_d": 9.0, "insert_depth": 15.0,
               "insert_dx": 50.8},
    # leveling: 1in surfacing bit, 3 passes of 0.5 (split into
    # 03 = pass 1 and 04 = passes 2..3 so a finished first pass is
    # never repeated)
    "level": {"tool_d": 25.4, "stepover": 19.0, "doc": 0.5,
              "passes": 3, "feed": 2500.0, "rpm": 16000},
    # tool table (F4): T1 = 1/4in end mill, T2 = 1in surfacing
    "gcode": {"tool_d": 6.35, "feed": 1800.0, "plunge": 500.0,
              "rpm": 18000, "stepdown": 4.0, "safe_z": 6.0,
              "overcut": 0.2, "tab_h": 3.0, "tab_w": 8.0},
}

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "output")


def _hdr(name, comments):
    return [f"({name} - spoilboard v{VERSION})"] + \
        [f"({c})" for c in comments]


def _park():
    pk = PARAMS["cnc"]["park"]
    return ["G53 Z0", f"G53 X{pk[0]:.3f} Y{pk[1]:.3f}"]


def _write(name, lines):
    with open(os.path.join(OUT, name + ".nc"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"  {name}.nc")


def _level_window():
    cn = PARAMS["cnc"]
    if cn.get("origin") and cn.get("travel"):
        return (-5.0, -5.0, cn["travel"][0] - cn["origin"][0] - 1.0,
                cn["travel"][1] - cn["origin"][1] - 1.0)
    return (0.0, 0.0, cn["bed"], cn["bed"])


def _level_serp(p):
    """One full serpentine of the level window at pass depth p*doc."""
    G = PARAMS["level"]
    x0, y0, rx, ry = _level_window()
    L = [f"(pass {p} of {G['passes']} - Z{-p * G['doc']:.3f})",
         "G0 Z6.00", f"G0 X{x0:.3f} Y{y0:.3f}",
         f"G1 Z{-p * G['doc']:.3f} F300"]
    y, left = y0, False
    while True:
        L.append(f"G1 X{x0 if left else rx:.3f} F{G['feed']:.0f}")
        left = not left
        if y + G["stepover"] <= ry - 1e-6:
            y += G["stepover"]
        elif y < ry - 1e-6:
            y = ry  # one forced final pass ON the far reach row
        else:
            break
        L.append(f"G1 Y{y:.3f} F{G['feed']:.0f}")
    return L


def write_set_zero():
    org = PARAMS["cnc"]["origin"]
    L = _hdr("00_set_work_zero", [
        f"G54 XY0 -> machine X{org[0]:.3f} Y{org[1]:.3f}",
        "slat corner + 15mm inset each axis - fence pins land in MDF",
        "parks the bit OVER the new XY0 as confirmation -",
        "M00 pause: check it, CYCLE START to park front-center",
        "Z offset untouched: re-touch per bit/stock"])
    L += ["G21 G90",
          f"G10 L2 P1 X{org[0]:.3f} Y{org[1]:.3f}",
          "G53 Z0",
          "G0 X0.000 Y0.000",
          "M00"] + _park() + ["M30"]
    _write("00_set_work_zero", L)


def write_level_test():
    G = PARAMS["level"]
    x0, y0, rx, ry = _level_window()
    L = _hdr("01_level_test", [
        "DRY RUN - spindle OFF, Z held at +10, nothing is cut",
        "first + last pass of 03_level: all 4 XY extremes",
        "runs clean = the leveling cannot trip a soft limit",
        "SAFE START: full Z retract + XY move off the toolsetter"])
    L += ["G21 G90 G94 G17",
          "G53 Z0",
          f"G0 X{x0:.3f} Y{y0:.3f}",
          "G0 Z10.00",
          f"G1 X{rx:.3f} F{G['feed']:.0f}",
          f"G0 Y{ry:.3f}",
          f"G1 X{x0:.3f} F{G['feed']:.0f}",
          "G0 X0.000 Y0.000"] + _park() + ["M30"]
    _write("01_level_test", L)


def write_tool_changes():
    for name, tnum, bit in (
            ("02_toolchange_surfacing", 2,
             "1in 25.4mm spoilboard surfacing bit"),
            ("06_toolchange_quarter", 1,
             "1/4in 6.35mm end mill - the everything bit")):
        L = _hdr(name, [
            f"M6 swap to T{tnum} = {bit}",
            "TOOLSETTER measures the new bit - work Z0 is kept",
            "do NOT re-touch Z after this file",
            "ends PARKED front-center at full height - never over "
            "the setter"])
        L += ["G21 G90",
              "M5",
              "G53 Z0",
              f"T{tnum} M6"] + _park() + ["M30"]
        _write(name, L)


def write_level():
    G = PARAMS["level"]
    x0, y0, rx, ry = _level_window()
    rad = G["tool_d"] / 2.0
    L = _hdr("03_level", [
        f"SURFACING bit d{G['tool_d']:.1f} - run after "
        "02_toolchange_surfacing",
        "Z0 = spoilboard HIGH point",
        f"pass 1 of {G['passes']} at Z{-G['doc']:.3f} - follow with "
        "04_level_deep for the rest",
        f"path X {x0:.0f}..{rx:.1f} Y {y0:.0f}..{ry:.1f} = machine "
        "reach - 1mm",
        f"coverage with this bit: X {x0 - rad:.1f}..{rx + rad:.1f} "
        f"Y {y0 - rad:.1f}..{ry + rad:.1f}",
        "SAFE START: full Z retract + XY move off the toolsetter"])
    L += ["G21 G90 G94 G17",
          "G53 Z0",
          f"G0 X{x0:.3f} Y{y0:.3f}",
          f"M3 S{G['rpm']:.0f}"]
    L += _level_serp(1)
    L += ["M5"] + _park() + ["M30"]
    _write("03_level", L)


def write_level_deep():
    G = PARAMS["level"]
    if G["passes"] < 2:
        return
    x0, y0, rx, ry = _level_window()
    doc = G["doc"]
    depths = ", ".join("%.1f" % (-p * doc)
                       for p in range(2, G["passes"] + 1))
    L = _hdr("04_level_deep", [
        f"SURFACING bit d{G['tool_d']:.1f} - follow-on passes "
        f"2..{G['passes']}",
        "SAME Z0 as 03_level - do NOT re-touch Z between the files",
        f"depths {depths} -> {G['passes'] * doc:.1f} total below Z0",
        "SAFE START: full Z retract + XY move off the toolsetter"])
    L += ["G21 G90 G94 G17",
          "G53 Z0",
          f"G0 X{x0:.3f} Y{y0:.3f}",
          f"M3 S{G['rpm']:.0f}"]
    for p in range(2, G["passes"] + 1):
        L += _level_serp(p)
    L += ["M5"] + _park() + ["M30"]
    _write("04_level_deep", L)


def write_level_edges():
    G = PARAMS["level"]
    x0, y0, rx, ry = _level_window()
    st = G["stepover"]
    groups = [("left", [x0, x0 + st]),
              ("right", [rx - 2 * st, rx - st, rx])]
    rad = G["tool_d"] / 2.0
    L = _hdr("05_level_edges", [
        f"SURFACING bit d{G['tool_d']:.1f} - side touch-up, "
        "front-to-back passes",
        "Z0 = the SAME leveling zero as 03_level",
        f"left strip covers X {x0 - rad:.1f}..{x0 + st + rad:.1f}; "
        f"right strip X {rx - 2 * st - rad:.1f}..{rx + rad:.1f}",
        f"{G['passes']} passes of {G['doc']:.1f} = "
        f"{G['passes'] * G['doc']:.1f} total - matches 03_level",
        "SAFE START: full Z retract + XY move off the toolsetter"])
    L += ["G21 G90 G94 G17",
          "G53 Z0",
          f"G0 X{x0:.3f} Y{y0:.3f}",
          f"M3 S{G['rpm']:.0f}"]
    for p in range(1, G["passes"] + 1):
        for _, cols in groups:
            L += ["G0 Z6.00",
                  f"G0 X{cols[0]:.3f} Y{y0:.3f}",
                  f"G1 Z{-p * G['doc']:.3f} F300"]
            at_far = False
            for i, cc in enumerate(cols):
                if i:
                    L.append(f"G1 X{cc:.3f} F{G['feed']:.0f}")
                L.append(f"G1 Y{y0 if at_far else ry:.3f} "
                         f"F{G['feed']:.0f}")
                at_far = not at_far
    L += ["M5"] + _park() + ["M30"]
    _write("05_level_edges", L)


def _ctr(c):
    return (sum(c) / len(c)) if isinstance(c, (tuple, list)) \
        else float(c)


QCW_PITCH, QCW_OUT_W = 9.5555 * 25.4, 9.875 * 25.4


def track_lines():
    """Slot centerlines in work coords: measured lines, or the
    one-touch ref anchor, or the pitch/offset fallback. Returns
    (lines, outer_w, verify_msg)."""
    tr = PARAMS["tracks"]
    lines = sorted(_ctr(c) for c in (tr.get("lines") or []))
    ow, vmsg = tr.get("outer_w"), None
    if not lines and tr.get("ref"):
        ri, rc = tr["ref"][0], _ctr(tr["ref"][1])
        lines = [rc + (i - ri) * QCW_PITCH for i in (1, 2, 3, 4)]
        if ow is None:
            ow = (QCW_OUT_W, QCW_OUT_W)
        if tr.get("verify"):
            vi, vc = tr["verify"][0], _ctr(tr["verify"][1])
            dev = vc - (rc + (vi - ri) * QCW_PITCH)
            vmsg = (f"one-touch verify: slot {vi} measured "
                    f"{dev:+.2f}mm off the manual prediction")
            print("  " + vmsg)
            if abs(dev) > 1.0:
                print("  *** TRACK GUARD: verify deviation > 1mm - "
                      "measure all six slots into tracks['lines']")
    if not lines and tr["pitch"] > 0:
        bed = PARAMS["cnc"]["bed"]
        c = tr["offset"] - tr["pitch"]
        while c <= bed + tr["pitch"]:
            lines.append(c)
            c += tr["pitch"]
    return lines, ow, vmsg


def write_track_targets():
    tr = PARAMS["tracks"]
    if tr.get("lines"):
        print("  07_track_targets skipped (lines fully measured)")
        return
    if tr.get("ref"):
        ri, rc = tr["ref"][0], _ctr(tr["ref"][1])
        xs = [rc + (i - ri) * QCW_PITCH for i in (1, 2, 3, 4)]
        src = "anchored to the measured ref touch"
    else:
        x1 = QCW_OUT_W + tr["track_gap"] / 2.0 - PARAMS["cnc"]["inset"]
        xs = [x1 + i * QCW_PITCH for i in range(4)]
        src = "manual p20 prediction - not measured yet"
    L = _hdr("07_track_targets", [
        f"parks over the 4 inner slot centers - {src}",
        "M00 pause at each: eyeball how far the bit is off center",
        "CYCLE START moves on; jogging is locked while paused",
        "REQUIRES the G54 WORKSPACE + work Z0 touched on a slat",
        "SAFE START: the bit parks OVER THE TOOLSETTER after an M6",
        "full Z retract and XY move away BEFORE coming down"])
    L += ["G21 G90", "G53 Z0"]
    for i, x in enumerate(xs):
        L.append(f"G0 X{x:.3f} Y100.000")
        if i == 0:
            L.append("G0 Z10.000")
        L.append("M00")
    L += _park() + ["M30"]
    _write("07_track_targets", L)
    print(f"    ({src}: {', '.join(f'{x:.1f}' for x in xs)})")


# ---------- bore/sheet emitter (for 08_pins + 09_insert_guide) -----
def _ctx(name, comments, rpm=None):
    G = PARAMS["gcode"]
    L = _hdr(name, comments + [
        "MASSO / ISO; single d%.2f end mill; units mm" % G["tool_d"],
        "SAFE START: full Z retract, XY move, only then Z down"])
    L += ["G21 G90 G94 G17",
          "G53 Z0",
          f"M3 S{(rpm or G['rpm']):.0f}"]
    first = [True]

    def rapid(x, y):
        L.append(f"G0 X{x:.3f} Y{y:.3f}")
        if first[0]:
            first[0] = False
            L.append(f"G0 Z{G['safe_z']:.2f}")

    def up():
        L.append(f"G0 Z{G['safe_z']:.2f}")

    return L, rapid, up


def _bore(L, rapid, up, cx, cy, d, final):
    """Peck (d ~ bit) or helix (d > bit) a bore to depth `final`
    (negative)."""
    G = PARAMS["gcode"]
    td = G["tool_d"]
    if d <= td + 0.2:
        rapid(cx, cy)
        z = 0.0
        while z > final + 1e-6:
            z = max(final, z - td)
            L.append(f"G1 Z{z:.3f} F{G['plunge']:.0f}")
            if z > final + 1e-6:
                L.append("G0 Z1.00")
        up()
        return
    rb = (d - td) / 2.0
    rapid(cx + rb, cy)
    L.append(f"G1 Z0.000 F{G['plunge']:.0f}")
    z = 0.0
    while z > final + 1e-6:
        z = max(final, z - min(G["stepdown"], 2.0))
        L.append(f"G2 X{cx + rb:.3f} Y{cy:.3f} I{-rb:.3f} J0.000 "
                 f"Z{z:.3f} F{G['plunge']:.0f}")
    L.append(f"G2 X{cx + rb:.3f} Y{cy:.3f} I{-rb:.3f} J0.000 "
             f"F{G['feed']:.0f}")
    up()


def write_pins():
    P = PARAMS
    bed, tr = P["cnc"]["bed"], P["tracks"]
    name = "08_pins"
    L, rapid, up = _ctx(name, [
        "SPOILBOARD workholding grid + sheet-alignment fence",
        "Z0 = SPOILBOARD top - re-run after each resurface",
        "fence: d8 blind 10 pins tangent to the X and Y zero lines",
        "grid: 3/4in dog holes @4in on slat centerlines, d9x15 "
        "EZ-LOK M6 insert bores +-2in staggered - all BLIND 15"])
    svg = []
    fence = []
    for v in (80.0, 610.0, 1140.0):
        fence += [(v, -4.0), (-4.0, v)]
    for (px, py) in fence:
        _bore(L, rapid, up, px, py, 8.0, -10.0)
        svg.append((px, py, 8.0))
    lines, ow, vmsg = track_lines()
    warned = False
    if lines:
        gd, step = tr["guard"], tr["grid"]
        rows = [(a + b) / 2.0 for a, b in zip(lines, lines[1:])]
        gh = tr["track_gap"] / 2.0
        sp = tr.get("span")
        if ow:
            rows = ([lines[0] - gh - ow[0] / 2.0] + rows
                    + [lines[-1] + gh + ow[1] / 2.0])
        elif sp:
            rows = ([(sp[0] + lines[0] - gh) / 2.0] + rows
                    + [(lines[-1] + gh + sp[1]) / 2.0])
        rows = sorted(set(r for r in rows if 30.0 <= r <= bed - 30.0))
        glines = list(lines)
        if ow and len(lines) == 4:
            glines = ([lines[0] - (tr["track_gap"] + ow[0])] + glines
                      + [lines[-1] + tr["track_gap"] + ow[1]])
        glines = [c for c in glines if -20.0 <= c <= bed + 20.0]
        for r in rows:
            v = 50.8
            while v <= bed - 50.8 + 0.01:
                x, y = (v, r) if tr["dir"] == "x" else (r, v)
                _bore(L, rapid, up, x, y, tr["dog_d"],
                      -tr["dog_depth"])
                svg.append((x, y, tr["dog_d"]))
                if v + step / 2.0 <= bed - 50.8:
                    for s in (-1.0, 1.0):
                        rr = r + s * tr["insert_dx"]
                        x, y = ((v + step / 2.0, rr)
                                if tr["dir"] == "x"
                                else (rr, v + step / 2.0))
                        _bore(L, rapid, up, x, y, tr["insert_d"],
                              -tr["insert_depth"])
                        svg.append((x, y, tr["insert_d"]))
                v += step
        for (px, py) in fence:
            cross = py if tr["dir"] == "x" else px
            near = min(abs(cross - c) for c in glines) \
                if glines else 1e9
            if near < gd:
                print(f"  *** TRACK GUARD: fence pin ({px:.0f},"
                      f"{py:.0f}) is {near:.1f} from a track "
                      f"(< {gd:.0f}) - SHIFT XY0, regenerate")
                warned = True
    else:
        print("  (08_pins: tracks not measured - fence pins only)")
    L += ["M5"] + _park() + ["M30"]
    _write(name, L)
    if warned:
        print("    *** DO NOT RUN 08 until the guard is clear")
    m = 30.0
    S = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox='
         f'"{-m} {-m} {bed + 2 * m} {bed + 2 * m}" '
         f'width="{(bed + 2 * m)}" height="{(bed + 2 * m)}">',
         f'<title>{name} - spoilboard v{VERSION}</title>',
         f'<rect x="0" y="0" width="{bed}" height="{bed}" '
         'fill="none" stroke="#999" stroke-dasharray="6,4" '
         'stroke-width="0.6"/>']
    for x, y, d in svg:
        S.append(f'<circle cx="{x}" cy="{y}" r="{d / 2}" '
                 'fill="none" stroke="#e07b00" stroke-width="0.6"/>')
    S.append("</svg>")
    with open(os.path.join(OUT, name + ".svg"), "w") as f:
        f.write("\n".join(S) + "\n")


def write_insert_guide():
    G = PARAMS["gcode"]
    td, r = G["tool_d"], G["tool_d"] / 2.0
    thru = -(18.0 + G["overcut"])
    name = "09_insert_guide"
    L, rapid, up = _ctx(name, [
        "INSERT DRIVER GUIDE - cut x2 from any 18mm offcut, stack "
        "on d8 pins + glue = 36 tall",
        "set over a spoilboard d9 bore; the d10.2 center bore keeps "
        "the M6x13 insert + 6mm hex bit square while driving",
        "flush-drive until the insert disappears below the block"])
    _bore(L, rapid, up, 30.0, 30.0, 10.2, thru)
    _bore(L, rapid, up, 15.0, 15.0, 8.0, thru)
    _bore(L, rapid, up, 45.0, 45.0, 8.0, thru)
    # outline 60x60 with 4 tabs
    tab_z = -(18.0 - G["tab_h"])
    pts = [(-r, -r), (60 + r, -r), (60 + r, 60 + r), (-r, 60 + r)]
    z = 0.0
    while z > thru + 1e-6:
        z = max(thru, z - G["stepdown"])
        rapid(*pts[0])
        L.append(f"G1 Z{z:.3f} F{G['plunge']:.0f}")
        for i in range(len(pts)):
            sx, sy = pts[i]
            ex, ey = pts[(i + 1) % len(pts)]
            seg = math.hypot(ex - sx, ey - sy)
            if z < tab_z and seg > 3 * G["tab_w"]:
                mx, my = (sx + ex) / 2, (sy + ey) / 2
                ux, uy = (ex - sx) / seg, (ey - sy) / seg
                L.append(f"G1 X{mx - ux * 4:.3f} Y{my - uy * 4:.3f} "
                         f"F{G['feed']:.0f}")
                L.append(f"G1 Z{tab_z:.3f} F{G['plunge']:.0f}")
                L.append(f"G1 X{mx + ux * 4:.3f} Y{my + uy * 4:.3f} "
                         f"F{G['feed']:.0f}")
                L.append(f"G1 Z{z:.3f} F{G['plunge']:.0f}")
            L.append(f"G1 X{ex:.3f} Y{ey:.3f} F{G['feed']:.0f}")
        up()
    L += ["M5"] + _park() + ["M30"]
    _write(name, L)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print(f"spoilboard v{VERSION}")
    write_set_zero()
    write_level_test()
    write_tool_changes()
    write_level()
    write_level_deep()
    write_level_edges()
    write_track_targets()
    write_pins()
    write_insert_guide()
    print("done -> cnc/output/")
