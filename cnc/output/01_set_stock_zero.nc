(01_set_stock_zero - spoilboard v0.7.2)
(G54 -> machine X18.184 Y68.584 Z5.400)
(programs the FULL workspace - no touching needed)
((Z works through the toolsetter tool offsets: any M6-)
(measured bit lands right))
(Z0 = TOP of 19.05mm stock on the slats (nominal 3/4in)
(board) - for sheet/part jobs. TEST then mic the real board,)
(set PARAMS stock.t to the ACTUAL, regenerate - the actual)
(also feeds thetable layer_t/ply_t. With no board loaded the)
(confirm tip stops 19.1 above the slats - a visual gap)
(check)
(confirmation: parks over XY0 then feeds DOWN to work Z0 -)
(the tip should kiss the expected surface at the zero point)
(M00: check all three zeros, CYCLE START parks front-center)
G21 G90
G10 L2 P1 X18.184 Y68.584 Z5.400
G53 Z0
G0 X0.000 Y0.000
G0 Z5.000
G1 Z0.000 F300
M00
G53 Z0
G53 X610.000 Y30.000
M30
