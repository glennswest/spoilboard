# Changelog

## [v0.8.0] — 2026-11-23

### Added
- **feat:** M8/M9 on every cutting file - the coolant relay runs
  the dust collection (matches crate v0.22.0 convention).

## [v0.7.2] — 2026-11-23

### Changed
- **revert:** flip dog back to full height (17 panel, 32 total) -
  owner: no need to shorten; the crate generators jump their
  rapids over the dogs (crate v0.18.1+). Do not print the v0.7.1
  short dog.

## [v0.7.1] — 2026-11-23

### Changed
- **fix:** flip dog panel section 17 -> 14 tall (total 29): with
  12mm crate stock the dog now stands ~2 proud of the panel and
  the Z+6 rapid plane clears by ~4 instead of ~1. Reprint 2.

## [v0.7.0] — 2026-11-18

### Changed
- **feat:** flip dog bed section is now CRUSH-RIB like the proven
  fence pin: 19.05 core + 8 ribs to OD 19.75, fits any dog hole
  19.15-19.75 and self-centers. Panel section stays PLAIN 19.3 -
  the panel must drop onto two dogs at once in the flip, so it
  keeps its designed clearance. flip_dog.scad synced.

## [v0.6.1] — 2026-11-18

### Fixed
- **fix:** crush-rib pin retuned 9.0->8.0 core (OD 9.7->8.7, fits
  holes 8.1-8.7). The "9.15 still loose" report was a STALE SLICER
  MESH - the owner's 3mf (saved 14:03) still held the 8.15 pin, so
  8.15 was printed twice. Bit confirmed 1/4in; the thrice-machined
  fence holes are realistically ~8.3-8.5, which 8.7-over-ribs covers.

## [v0.6.0] — 2026-11-18

### Changed
- **feat:** fence pin fit section is now CRUSH-RIB: 9.0 core + six
  ribs 0.35 proud (9.7 over ribs, 0.92 lead-in taper). One print
  fits any hole 9.1-9.7 - the ribs shave to size and self-center,
  so the 8.00 datum stays on the fence line. Plain 8.05/8.15/9.15
  pins all tested loose; the holes are far over the nominal 8.0,
  which points at the CHUCKED BIT being over 6.35 (or heavy runout)
  - VERIFY THE BIT before cutting crate2.

## [v0.5.0] — 2026-11-18

### Added
- **feat:** printed PLUG GAUGES - stepped pucks that measure the
  holes without calipers: `fence_gauge.stl` (bands 8.2-9.0 x 2) and
  `dog_gauge.stl` (bands 19.1-19.5 x 3). Push in until it stops;
  the first band still showing = hole is smaller than that band.

### Changed
- **fix:** fence pin fit section 8.15 -> 9.15 (owner: still loose
  fully seated - the re-machined holes are well over nominal; the
  gauges will pin down the real number). Datum stays 8.00.

## [v0.4.1] — 2026-11-18

### Fixed
- **fix:** fit pucks printed LOOSE on both (owner's test): +0.1
  print compensation on every fit diameter — flip dog bed 19.0 ->
  19.1 / panel 19.2 -> 19.3, fence pin fit 8.05 -> 8.15. The fence
  pin DATUM section stays 8.00 modeled: mic the printed datum and
  add any shortfall to FP_DATUM_D (the as-printed datum must BE
  8.00 — it sets the fence line). flip_dog.scad kept in sync.
- **fix:** v0.4.0 accidentally overwrote CHANGELOG.md with the
  CLAUDE.md contents — history restored from git; CLAUDE.md and
  cnc/generate.py versions re-synced (both had been left behind).

## [v0.4.0] — 2026-11-18

### Added
- **feat:** `print/` fence pins — printable two-step d8 pins for
  the fence holes (owner: shelf d8 pins too loose). FP_BED_D 8.05
  fit section ×10 deep + FP_DATUM_D 8.00 bearing section ×15
  stick-up, 1.2 chamfer; `fence_pin.stl` (print SIX) +
  `fence_pin_test.stl` 7 mm fit puck (print FIRST).

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
