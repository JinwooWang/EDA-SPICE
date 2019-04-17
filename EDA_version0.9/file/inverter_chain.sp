*Inverter
v1 1 0 pulse(0 3 1ns 1ns 1ns 10ns 20ns)
v2 7 0 3
M1 2 1 0 0 MOD1 W=2 L=1
M2 2 1 7 7 MOD2 W=10 L=1
M3 3 2 0 0 MOD1 W=2 L=1
M4 3 2 7 7 MOD2 W=10 L=1
M5 4 3 0 0 MOD1 W=2 L=1
M6 4 3 7 7 MOD2 W=10 L=1
M7 5 4 0 0 MOD1 W=2 L=1
M8 5 4 7 7 MOD2 W=10 L=1
M9 6 5 0 0 MOD1 W=2 L=1
M10 6 5 7 7 MOD2 W=10 L=1
*.dc v1 0 3 0.05
.tran 1ns 22ns
.MODEL MOD1 NMOS
.MODEL MOD2 PMOS

.end
