# spoilboard — Onefinity Foreman Elite machine + QCW spoilboard setup

Two things live here: the owner's QCW replacement-slat designs
(OpenSCAD + SVG, from the official manual diagram) and, since
2026-11-13, the MACHINE setup cut files extracted from
glennswest/thetable — everything that belongs to the machine rather
than to any furniture project.

## Version
- Current: **0.1.1**
- Version locations: this file, `CHANGELOG.md`, `cnc/generate.py`

## Cut files (`python3 cnc/generate.py` → `cnc/output/`, numbered
stick-ready; `python3 cnc/stick.py` → /Volumes/MASSO/spoilboard/)
- 00_set_work_zero — G54 XY0 → machine (18.184, 68.584); confirms
  by feeding the tip DOWN TO Z0 at the zero point (M00), needs work
  Z0 touched first
- 01_level_test — dry run of the leveling extents
- 02_toolchange_surfacing / 06_toolchange_quarter — toolsetter M6
- 03_level / 04_level_deep / 05_level_edges — the skim (3 × 0.5,
  split so a finished pass is never repeated; SAME Z0 throughout)
- 07_track_targets — M00 parks over the measured slot centers
- 08_pins — fence pins + ¾″ dog holes + ∅9×15 M6 insert bores
- 09_insert_guide — driver jig for the M6×13 inserts (cut ×2)

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

## Conventions
- Same as thetable: mm, MASSO ISO dialect, Z0 = stock/spoilboard
  top, semver + changelog, no Claude attribution in commits.
