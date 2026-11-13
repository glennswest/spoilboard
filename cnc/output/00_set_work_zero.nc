(00_set_work_zero - spoilboard v0.1.1)
(G54 XY0 -> machine X18.184 Y68.584)
(slat corner + 15mm inset each axis - fence pins land in MDF)
(REQUIRES work Z0 already touched on the surface)
(confirmation: parks over XY0 then feeds DOWN to Z0 - the)
(bit tip should kiss the touch surface exactly at the zero)
(point. M00 pause: check all three zeros, CYCLE START parks)
(a Z soft limit here = work Z0 was never touched)
G21 G90
G10 L2 P1 X18.184 Y68.584
G53 Z0
G0 X0.000 Y0.000
G0 Z5.000
G1 Z0.000 F300
M00
G53 Z0
G53 X610.000 Y30.000
M30
