(02_level_test - spoilboard v0.2.0)
(DRY RUN - spindle OFF, Z held at +10, nothing is cut)
(first + last pass of 04_level: all 4 XY extremes)
(runs clean = the leveling cannot trip a soft limit)
(SAFE START: full Z retract + XY move off the toolsetter)
G21 G90 G94 G17
G53 Z0
G0 X-5.000 Y-5.000
G0 Z10.00
G1 X1200.814 F2500
G0 Y1159.134
G1 X-5.000 F2500
G0 X0.000 Y0.000
G53 Z0
G53 X610.000 Y30.000
M30
