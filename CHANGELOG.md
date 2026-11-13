# Changelog

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
