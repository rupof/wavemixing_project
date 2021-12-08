from plots.multi_plots import get_rho_ss_list
from post_processing.local_calculations.get_cs_from_given_rho_ss import * 

import numpy as np

N = 5
Omega = 2.0
Delta = 20.0
useb0 = 1
b0 = 0.1
description = f"b0_{b0}_V_Int_On"
rho_ss_parameter = "direct"
ang1 = 25

rho_ss_list = get_rho_ss_list(N, Omega, Delta, description, rho_ss_parameter= rho_ss_parameter, results_path="../results/")


for rho_ss in rho_ss_list:
    try:
        get_cs_for_a_rho_ss(ang1, 0, N, useb0, b0, None, description, 1, Omega, Delta, rho_ss_parameter, 0, rho_ss) 
    except:
        print("error in ", rho_ss)

