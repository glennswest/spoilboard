(00_set_work_zero - spoilboard v0.1.0)
(G54 XY0 -> machine X18.184 Y68.584)
(slat corner + 15mm inset each axis - fence pins land in MDF)
(parks the bit OVER the new XY0 as confirmation -)
(M00 pause: check it, CYCLE START to park front-center)
(Z offset untouched: re-touch per bit/stock)
G21 G90
G10 L2 P1 X18.184 Y68.584
G53 Z0
G0 X0.000 Y0.000
M00
G53 Z0
G53 X610.000 Y30.000
M30
