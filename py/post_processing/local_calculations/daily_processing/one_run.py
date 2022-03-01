from post_processing.local_calculations.get_g2 import * 
from post_processing.local_calculations.get_cs import * 



N = 1
Omega = 0.02
Delta = 0.0
useb0 = 1
kd = None
b0 = 0.1
description = f"b0_{b0}_V_Int_On_teste"
description = f"OffTeste_same_pos_b0_0.1_"
rho_ss_parameter = "direct"
ang1 = 25
ang2 = 25
interaction = True
tmax=0

get_g2_from_all_available_rho_ss(ang1,ang2, N, useb0, b0, kd, description, interaction, Omega, Delta, rho_ss_parameter, tmax)

