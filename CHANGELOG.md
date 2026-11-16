# Changelog

## [v0.3.3] — 2026-11-16

### Fixed
- **fix:** 3/4in dog holes left a STANDING CORE (owner's photo:
  "big holes with a core :(") - _bore cut a single orbit at one
  radius, clearing only an annulus; in blind holes the center
  stub stays attached. Bores now spiral inside-out per depth
  level (first orbit overlaps center; verified coverage 0 ->
  9.53 >= hole radius). Re-running the file machines the
  existing cores away.

## [v0.3.2] — 2026-11-16

### Fixed
- **fix:** the remaining hopping was the FENCE PINS (owner
  rewound and watched from the start): they alternated bottom
  edge / left edge, criss-crossing the full bed six times before
  the grid even began. Now: bottom edge right-to-left, around
  the corner, up the left edge, then the grid starts its first
  line from the top - total rapid travel 21.1 -> 16.6 m and zero
  cross-bed moves.

## [v0.3.1] — 2026-11-16

### Fixed
- **fix:** 09_pins drilling order (owner stopped the cut: "order
  is all over the place") - the grid interleaved dog and insert
  bores with +-100 side-hops at every hole. Now emitted as 15
  straight vertical lines serpentined across the bed: monotone
  climbs, two direction changes per slat instead of seventy.
  RE-SYNC THE STICK before cutting.

## [v0.3.0] — 2026-11-14

### Added
- **feat:** `print/` — 3D-printed ¾″ flip-registration dogs for the
  crate1/crate2 full-sheet flip route (print TWO). Two-step design:
  Ø19.0 × 15 bed section (snug in the ∅19.05 grid holes) + Ø19.2 × 17
  panel section (0.15 clearance in the panel's ∅19.35 bores — tighter
  registration than a ¾″ dowel's 0.3), 2 mm top chamfer, 0.5
  elephant-foot relief, 32 total (17 stick-up = 4 proud of a 13
  panel, 2 under the Z+6 rapid plane; never exceed 33). Parametric
  `flip_dog.scad` + dependency-free `make_stl.py` emitting committed
  print-ready `flip_dog.stl` and an 8 mm `flip_dog_test.stl` bed-fit
  puck (print first, adjust diameters in 0.05 steps).

## [v0.2.0] — 2026-11-13

### Added
- **feat:** PROGRAMMED Z zeros (owner): 00_set_work_zero now sets
  the full XYZ workspace with Z0 at the measured spoilboard surface
  (G54 Z −13.650 — valid through the toolsetter offsets for any
  M6-measured bit; stale after a re-skim). NEW 01_set_stock_zero
  puts Z0 at the top of nominal ¾″ stock (+19.05); the owner
  test-cuts, mics the actual, PARAMS stock.t gets the real number
  (which also feeds thetable layer_t/ply_t). Files 01–09 renumbered
  02–10.

## [v0.1.1] — 2026-11-13

### Changed
- **feat:** 00_set_work_zero confirmation now proves ALL zeros
  (owner): after parking over XY0 it feeds down (F300) to work Z0 -
  the bit tip kisses the touch surface exactly at the zero point,
  M00, then parks. Requires Z0 touched first; a stale/missing Z
  offset trips the soft limit instead of diving.

## [v0.1.0] — 2026-11-13

### Added
- **feat:** machine + spoilboard setup cut files extracted from
  glennswest/thetable v0.51.0 into their own repo (owner: each
  project its own github + its own numbered folder on the stick):
  00_set_work_zero … 09_insert_guide, all stick-ready numbered from
  zero, SAFE START + front park in every file, track anchor and
  measured machine geometry carried over. 08_pins verified
  coordinate-identical (161 bores) against thetable's
  spoilboard_pins. cnc/stick.py syncs /Volumes/MASSO/spoilboard/.
