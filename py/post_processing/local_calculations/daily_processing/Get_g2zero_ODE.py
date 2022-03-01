from post_processing.local_calculations.get_g2 import * 
from post_processing.local_calculations.get_cs import * 



N = 10
Omega = 2.0
Delta = 20.0
useb0 = 1
kd = None
b0 = 0.1
description = f"b0_{b0}_V_Int_On_testeODE_t01_"
interaction = 1
rho_ss_parameter = "direct"
ang1 = 25
ang2 = 25
interaction = True
tmax=0

get_g2_zero_from_all_available_rho_ss( N, useb0, b0, kd, description, interaction, Omega, Delta, rho_ss_parameter, tmax  )


