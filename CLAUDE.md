# spoilboard — Onefinity Foreman Elite machine + QCW spoilboard setup

Two things live here: the owner's QCW replacement-slat designs
(OpenSCAD + SVG, from the official manual diagram) and, since
2026-11-13, the MACHINE setup cut files extracted from
glennswest/thetable — everything that belongs to the machine rather
than to any furniture project.

## Version
- Current: **0.5.0**
- Version locations: this file, `CHANGELOG.md`, `cnc/generate.py`

## Cut files (`python3 cnc/generate.py` → `cnc/output/`, numbered
stick-ready; `python3 cnc/stick.py` → /Volumes/MASSO/spoilboard/)
- 00_set_work_zero — programs the FULL workspace XYZ: Z0 = the
  SPOILBOARD surface (G54 Z −13.650, measured; works through the
  toolsetter offsets, no touching). STALE after any re-skim.
- 01_set_stock_zero — Z0 = top of nominal ¾″ stock on the slats
  (−13.650 + stock.t 19.05). Owner test-cuts, mics the real board →
  stock.t ACTUAL → regenerate; the actual feeds thetable layer_t.
- 02_level_test — dry run of the leveling extents
- 03_toolchange_surfacing / 07_toolchange_quarter — toolsetter M6
- 04_level / 05_level_deep / 06_level_edges — the skim (3 × 0.5,
  split so a finished pass is never repeated; SAME Z0 throughout)
- 08_track_targets — M00 parks over the measured slot centers
- 09_pins — fence pins + ¾″ dog holes + ∅9×15 M6 insert bores
- 10_insert_guide — driver jig for the M6×13 inserts (cut ×2)
Both zero files confirm by feeding the tip down to work Z0 over the
zero point (M00) — all three zeros proven visually.

## Machine facts (measured)
- G54 XY0 = machine (18.184, 68.584); travel (1220.0, 1228.7);
  G54 Z ref −13.650 (slat top after the −1.5 skim; Masso F4 shows
  inches). Park = machine (610, 30) at full height, every file.
- Track anchor (2026-11-12): slot centers work X 227.9 / 470.6 /
  713.3 / 956.0 (ref slot 1 = 227.871, manual-p20 pitch exact).
- Tool table: T1 = ¼″ end mill, T2 = 1″ surfacing. Golden rules:
  home WITH a bit chucked; after homing only change bits via M6; an
  M6 to the already-loaded tool is ignored (swap away and back to
  re-measure). SAFE START in every file: G53 Z0 → XY → only then Z.
- Workholding: brad/pin-nail stock to the slats in waste zones
  (owner has a pneumatic nailer) — nails ≥15 mm from any cut line;
  the 08 grid (dogs + inserts) is the screw-down alternative.
- Fence pins (`print/`, v0.5.0): printed two-step d8 pins for the
  fence holes (shelf pins too loose) — 9.15 fit + 8.00 DATUM section
  (the bearing surface IS the fence line: mic the printed datum, add
  any shortfall to FP_DATUM_D); print SIX, test puck first.
- Flip dogs (`print/`, v0.4.1): 3D-printed two-step ¾″ dogs for the
  crate full-sheet flip route — `flip_dog.stl` ×2 (Ø19.1×15 bed +
  Ø19.3×17 panel sections, 32 total; never exceed 33 = 18 stick-up),
  `flip_dog_test.stl` fit puck first. All fit diameters carry +0.1
  print comp (v0.4.1, pucks tested loose). Params in flip_dog.scad /
  make_stl.py (keep in sync); regenerate with `python3 print/make_stl.py`.

## Conventions
- Same as thetable: mm, MASSO ISO dialect, Z0 = stock/spoilboard
  top, semver + changelog, no Claude attribution in commits.
