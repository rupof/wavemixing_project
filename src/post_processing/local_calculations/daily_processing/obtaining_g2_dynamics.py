from single_and_double_excitations_subspace.parameter_generator_for_ODE import *
from single_and_double_excitations_subspace.atomic_contributions_ODE import *
from single_and_double_excitations_subspace.QRT_dynamics_ODE import *
from file_manager.visualization_preparation_tools import *


import os
import sys



ang2 = 205
R1 = get_nhat_from_angle(25)
N = 5
tf = 1
Omega = 2.0
Delta = 20.0
b0 = 0.1

R2 = get_nhat_from_angle(ang2)
N_atoms = N
N_runs = 20
taulist, dt = np.linspace(0,tf,100, retstep = True) 

r_list = [ random_cloud(0, N, exc_radius = None, b0 = b0) for i in range(N_runs)]

for r in r_list:
    #Approximated
    Delta1D, Omega1D, Gamma2D, Delta2D  = GetAllODEParametersGiven_r(Omega, Delta, r, scalar = True)
    Beta1D, Beta2D, t_span, r = SolveForBeta1DandBeta2D_tau_QRT(N, kd = None , b0 = None, exc_radius = None, Delta = Delta , Omega = Omega, wave_mixing = True, scalar = True, interaction = True, r = r, taulist=t_span, Sm_1D = S_sigmam_i_expectations, Sm_2D = S_sigmam_ij_expectations )

    g2_list = np.zeros_like(t_span)
    for t in range(len(t_span)):
            g2_list[t] = np.real(g2_of_zero_subspace_approach(r, R1, R2, Beta1D[t], Beta2D[t]))

    #Exact
    S_H, S_c_ops, GTensor,M, GammaSR, DeltaSR, Omega, SR_state, r = system_spec_N(1, N_atoms, kd = None, b0 = None, exc_radius = None , Delta = Delta, Omega = Omega, wave_mixing = True, scalar = True, r = r)
    rho_ss_S, total_time_ss = get_steadystate(S_H, 0, r,  0, S_c_ops, N_atoms, faseglobal = 1, rho_ss = None, rho_ss_parameter = "direct", tmax = None)
    g2_ls, rho_ss, total_time_ss, total_time_correlation = g2_l(S_H, 0, r, R1, R2, taulist, S_c_ops, N, faseglobal = 1, rho_ss = rho_ss_S, rho_ss_parameter = "direct", tmax = None)
    

print("oi")





