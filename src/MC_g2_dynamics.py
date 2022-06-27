import numpy as np
from qutip import *
from timeit import default_timer as timer

from helper_functions.interaction_preparation import *
from helper_functions.operators import *
from helper_functions.other import *

from hamiltonian.hamiltonian_builder import *
from hamiltonian.different_waves import *

from correlation.second_order_correlation import *

from post_processing.local_calculations.get_g2 import *

from file_manager import *
import sys
#from single_and_double_excitations_subspace.atomic_contributions_ODE import *
from single_and_double_excitations_subspace.atomic_contributions_optimized_ODE import *
from single_and_double_excitations_subspace.MC_dynamics_ODE import *

import matplotlib.pyplot as plt

start = timer()


# t_span, dt = np.linspace(0,100, 100, retstep = True )

r = None

Gamma = 1
nhat = 0


ang1 = float(sys.argv[1])  # this is a useless parameter
print(f"ang1 = {ang1}")
ang2 = float(sys.argv[2])  # This is a useless parameter
print(f"ang2 = {ang2}")
N = int(sys.argv[3])
print(f"N = {N}")
useb0 = bool(int(sys.argv[4]))
print(f"useb0 = {useb0}")
if useb0 == True:
    b0 = float(sys.argv[5])
    kd = None
    exc_radius = None
    description = str(sys.argv[6])
    print(f"b0 = {b0}, description = {description}")
    # ang1 ang2 N useb0 b0 description interaction Omega Delta
else:
    b0 = None
    kd = float(sys.argv[5])
    exc_radius = float(sys.argv[6])
    description = str(sys.argv[7])
    # ang1 ang2 N useb0 kd exc_radius description
    print("kd main", kd)
interaction = bool(int(sys.argv[7]))
print(f"interaction = {interaction}")
Omega = float(sys.argv[8])*Gamma
print(f"Omega = {Omega}")
Delta = float(sys.argv[9])*Gamma
print(f"Delta = {Delta}")
rho_ss_parameter = str(sys.argv[10])  # useless
print(f"rho_ss_parameter = {rho_ss_parameter}")
tmax = float(sys.argv[11])  # useless
print(f"tmax = {tmax}")
steady_state_path = str(sys.argv[12])

if steady_state_path == "None":
    results_path = "../results/"
    DefaultInfo = f"N{N}_Omega{Omega}_Delta{Delta}_"
    steady_state_path = results_path+DefaultInfo + \
        description + "_" + rho_ss_parameter + "/"
print(f"steady_state_path={steady_state_path}")

theta = float(sys.argv[13])  # inclination angle
print(f"theta ={theta}")
single_excitation = bool(int(sys.argv[14]))
print(f"single_excitation ={single_excitation}")

wave_mixing = True
scalar = True
description += f'_{rho_ss_parameter}'  # useless

if tmax != 0:
    description += f'_{tmax}'
###########################################

tf = 5  # shorter time
taulist, dt = np.linspace(0, tf, 200, retstep=True)
R1 = get_nhat_from_angle(ang1, theta)
R2 = get_nhat_from_angle(ang2, theta+180)


paths_array_containing_theta_files = get_array_of_runs_dat_files(
    steady_state_path)  # all runs for a given phi

paths_array = [run_name for run_name in paths_array_containing_theta_files if "theta" not in run_name ]



runs_txt = get_array_of_numpy_runs(paths_array, npy=True)
Beta1D_t, Beta2D_t, t_span, r = runs_txt[0][0], runs_txt[0][1], runs_txt[0][2], runs_txt[0][3]
Beta1D_steady_state, Beta2D_steady_state = Beta1D_t[-1], Beta2D_t[-1]


Beta1D_projected_state = get_Beta1D_projected_state(r, Beta1D_steady_state, Beta2D_steady_state,
                                                    R1, optimized=True)
if single_excitation == False:
    Beta1D_tau, Beta2D_tau, taulist, r = SolveForBeta1DandBeta2D_optimized(N, kd=None, b0=None,
                                                                           exc_radius=None, Delta=Delta,
                                                                           Omega=Omega, wave_mixing=wave_mixing,
                                                                           scalar=scalar, interaction=interaction,
                                                                           r=r, t_span=taulist,
                                                                           initial_Beta1D=Beta1D_projected_state)
   
    G2_MonteCarlo, I_MonteCarlo = get_g2(r, Beta1D_steady_state, Beta2D_steady_state,
                                   Beta1D_tau, Beta2D_tau, R1, R2, optimized=True)

    G2_MonteCarlo_single_excitation, I_MonteCarlo_single_excitation = get_g2(r, Beta1D_steady_state, Beta2D_steady_state,
                           Beta1D_tau, None, R1, R2, optimized=True)


    G2_MonteCarlo_same_direction, I_MonteCarlo_same_direction= get_g2(r, Beta1D_steady_state, Beta2D_steady_state,
                                                Beta1D_tau[:1], Beta2D_tau[:1], R1, R1, optimized=True)

    G2_MonteCarlo_single_excitation_same_direction, I_MonteCarlo_single_excitation_same_direction= get_g2(r, Beta1D_steady_state, Beta2D_steady_state, Beta1D_tau[:1], None, R1, R1, optimized=True)


    files_to_save = [G2_MonteCarlo, G2_MonteCarlo_single_excitation, G2_MonteCarlo_same_direction, G2_MonteCarlo_single_excitation_same_direction,  I_MonteCarlo, I_MonteCarlo_single_excitation, I_MonteCarlo_same_direction, I_MonteCarlo_single_excitation_same_direction, taulist]
else:
    Beta1D_tau, taulist, r = SolveForBeta1D_optimized(N, kd=None, b0=None,
                                                      exc_radius=None, Delta=Delta,
                                                      Omega=Omega, wave_mixing=True,
                                                      scalar=scalar, interaction=interaction,
                                                      r=r, t_span=taulist,
                                                      initial_Beta1D=Beta1D_projected_state)
    Beta2D_tau = None

    G2_MonteCarlo_single_excitation, I_MonteCarlo_single_excitation = get_g2(r, Beta1D_steady_state, Beta2D_steady_state,
                           Beta1D_tau, None, R1, R2, optimized=True)
    
    G2_MonteCarlo_single_excitation_same_direction, I_MonteCarlo_single_excitation_same_direction= get_g2(r, Beta1D_steady_state, Beta2D_steady_state,
                           Beta1D_tau[:1], None, R1, R1, optimized=True)


    files_to_save = [G2_MonteCarlo_single_excitation, G2_MonteCarlo_single_excitation_same_direction, I_MonteCarlo_single_excitation, I_MonteCarlo_single_excitation_same_direction, taulist]

endODE = timer()


variables = r"$ \Gamma={0}, \Omega={1} \Gamma, \Delta = {2} , kd = {3}, N = {4}, b0 = {5} $".format(
    Gamma, Omega, Delta, kd, N, b0)

variables_string = "Gamma={0} \nOmega={1}*Gamma \nDelta = {2} \nkd = {3} \nN = {4}  \nb0 = {5}\nscalar = {6}, interaction = {7} ".format(
    Gamma, Omega, Delta, kd, N, b0, scalar, interaction)


end = timer()

# Saving files!


path_to_save_file = get_path_to_save_files(N, Omega, Delta,  description)
filename = "{4}/N{3}_Omega{5}_Delta{6}_run".format(
    ang1, ang2, 0, N, path_to_save_file, Omega, Delta)

run_number = get_new_run_number_dat(filename)-1 #temporary fix so that steady state number coincides with correlation run number

name_of_file = "{4}/N{3}_Omega{5}_Delta{6}_theta{7}_run{2}".format(
    ang1, ang2, run_number, N, path_to_save_file, Omega, Delta, theta)
name_of_file_time = "{4}time/time_N{3}_Omega{5}_Delta{6}_theta{7}_run{2}.txt".format(
    ang1, ang2, run_number, N, path_to_save_file, Omega, Delta, theta)
name_of_file_r = "{4}positions/positions_N{3}_Omega{5}_Delta{6}_theta{7}_run{2}".format(
    ang1, ang2, run_number, N, path_to_save_file, Omega, Delta, theta)


save_params_to_file(variables_string, filename)

# saving time Total, ODE, g2zero
#np.savetxt(name_of_file_time, [end - start, endODE-start, end-endODE])
np.save(name_of_file, [*files_to_save])  # saving betas
#save_rhoss_to_file(r, name_of_file_r)  # saving positions


#fig, ax = plt.subplots()
#ax.plot(taulist, np.real(g2_lig)   )
# fig.savefig("testinho.png")
# plt.show()

print(description)
print("PROGRAM FINISHED.\n Total time: ", end - start)  # Time
