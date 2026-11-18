// flip_dog — 3D-printed ¾″ registration dog for the QCW dog grid
//
// Used in pairs for the crate1/crate2 full-sheet flip route: the short
// run bores two ∅19.35 holes in the panel over bed dog holes; the
// panel flips left-right onto two of these dogs in the mirror column.
//
// Two-step design (better than a plain dowel):
//   - bed section  Ø19.1 × 15  — snug push fit in the ∅19.05 × 15 bed hole
//   - panel section Ø19.3 × 17 — 0.05 total clearance in the ∅19.35
//     panel bore (vs 0.3 for a dowel) → tighter flip registration
//   - total 32 tall → 17 stick-up = 4 proud of a 13 panel, clears the
//     Z+6 rapid plane by 2. NEVER print taller than 33 (18 stick-up max).
//
// Print: vertical as modeled, PLA or PETG, 5+ perimeters, any infill,
// 0.2 layers. Printers vary ±0.1 on cylinder diameter — print
// flip_dog_test.stl (8 mm puck) first, test in a bed hole, and trim
// bed_d / panel_d by 0.05 steps until snug (bed) / easy drop (panel).

bed_core = 19.05;  // crush-rib bed: core diameter (hole nominal)
bed_rib  = 0.35;   // 8 ribs this proud -> OD 19.75, fits 19.15-19.75
panel_d  = 19.3;   // panel-hole section PLAIN (bore is 19.35)
bed_h    = 15.0;   // bed hole depth
panel_h  = 17.0;   // stick-up above the slat
ch_top   = 2.0;    // top lead-in chamfer
ch_bot   = 0.5;    // elephant-foot relief
$fn      = 128;

module dog() {
    // ribbed bed section: core + 8 crush ribs (shave to fit)
    union() {
        cylinder(d = bed_core, h = bed_h);
        for (i = [0:7]) rotate([0, 0, i * 45])
            translate([0, -1.25, 1.5])
                cube([bed_core/2 + bed_rib, 2.5, bed_h - 1.5]);
        dog_upper();
    }
}

module dog_upper() {
    rotate_extrude() polygon([
        [0, 0],
        [bed_core/2 - ch_bot, 0],
        [bed_core/2, ch_bot],
        [bed_core/2, bed_h],
        [panel_d/2, bed_h],
        [panel_d/2, bed_h + panel_h - ch_top],
        [panel_d/2 - ch_top, bed_h + panel_h],
        [0, bed_h + panel_h],
    ]);
}

dog();
