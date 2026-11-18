(08_track_targets - spoilboard v0.7.0)
(parks over the 4 inner slot centers - anchored to the measured ref touch)
(M00 pause at each: eyeball how far the bit is off center)
(CYCLE START moves on; jogging is locked while paused)
(REQUIRES the G54 WORKSPACE + work Z0 touched on a slat)
(SAFE START: the bit parks OVER THE TOOLSETTER after an M6)
(full Z retract and XY move away BEFORE coming down)
G21 G90
G53 Z0
G0 X227.871 Y100.000
G0 Z10.000
M00
G0 X470.581 Y100.000
M00
G0 X713.290 Y100.000
M00
G0 X956.000 Y100.000
M00
G53 Z0
G53 X610.000 Y30.000
M30
