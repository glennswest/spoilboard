(00_set_work_zero - spoilboard v0.7.1)
(G54 -> machine X18.184 Y68.584 Z-13.650)
(programs the FULL workspace - no touching needed)
((Z works through the toolsetter tool offsets: any M6-)
(measured bit lands right))
(Z0 = the SPOILBOARD surface (measured 2026-11-12,)
(-0.53740in on the F4 screen) - for slat jobs: 09_pins,)
(re-skims. STALE AFTER ANY RE-SKIM: re-touch, update g54_z,)
(regenerate)
(confirmation: parks over XY0 then feeds DOWN to work Z0 -)
(the tip should kiss the expected surface at the zero point)
(M00: check all three zeros, CYCLE START parks front-center)
G21 G90
G10 L2 P1 X18.184 Y68.584 Z-13.650
G53 Z0
G0 X0.000 Y0.000
G0 Z5.000
G1 Z0.000 F300
M00
G53 Z0
G53 X610.000 Y30.000
M30
