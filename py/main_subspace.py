import matplotlib.pyplot as plt
import numpy as np
from qutip import *
from timeit import default_timer as timer
from helper_functions.interaction_preparation import *
from helper_functions.operators import *
from helper_functions.other import * 
from hamiltonean_builder.hamiltonean_builder import *
from correlation.second_order_correlation import *
from post_processing.local_calculations.get_g2 import *

from file_manager import *
import sys
from single_and_double_excitations_subspace.atomic_contributions_ODE import *



start = timer()



t_span, dt = np.linspace(0,100, 100, retstep = True ) 
r = None

Gamma = 1
nhat = 0



ang1 = float(sys.argv[1]) ##this is a useless parameter
print(f"ang1 = {ang1}")
ang2 = float(sys.argv[2]) ##This is a useless parameter
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
rho_ss_parameter = str(sys.argv[10]) # useless
print(f"rho_ss_parameter = {rho_ss_parameter}")
tmax = float(sys.argv[11]) # useless
print(f"tmax = {tmax}")



get_g2zero_full = True
wave_mixing = True
scalar = True



description += f'_{rho_ss_parameter}' # useless

if tmax != 0:
    description += f'_{tmax}'


Beta1D, Beta2D, t_span, r = SolveForBeta1DandBeta2D(N, kd , b0, exc_radius , Delta , Omega, wave_mixing, scalar, interaction, r, t_span)

Beta1D_list = Beta1D
Beta2D_list = Beta2D

if get_g2zero_full == True:
    run_number = get_all_g2_zero_for_a_beta(r, Beta1D_list, Beta2D_list, N, useb0, b0, kd, description, interaction, Omega, Delta )




variables = r"$ \Gamma={0}, \Omega={1} \Gamma, \Delta = {2} , kd = {3}, N = {4}, b0 = {5} $".format(Gamma,Omega, Delta, kd, N, b0)

variables_string = "Gamma={0} \nOmega={1}*Gamma \nDelta = {2} \nkd = {3} \nN = {4}  \nb0 = {5}\nscalar = {6}, interaction = {7} ".format(Gamma,Omega, Delta, kd, N, b0, scalar , interaction)



end = timer()

#Saving files!

        
path_to_save_file = get_path_to_save_files(N, Omega, Delta,  description)
filename ="{4}/N{3}_Omega{5}_Delta{6}_run".format(ang1,ang2,0,N,path_to_save_file, Omega, Delta) 

if get_g2zero_full == False:
    run_number = get_new_run_number_dat(filename)

name_of_file =  "{4}/N{3}_Omega{5}_Delta{6}_run{2}".format(ang1,ang2,run_number,N, path_to_save_file, Omega, Delta)
name_of_file_time =  "{4}/time/time_N{3}_Omega{5}_Delta{6}_run{2}.txt".format(ang1,ang2,run_number,N, path_to_save_file, Omega, Delta)

#name_of_file_hamiltonean ="{4}/hamiltonean/hamiltonean_N{3}_Omega{5}_Delta{6}_run{2}".format(ang1,ang2,run_number,N, path_to_save_file, Omega, Delta)

#name_of_file_c_ops ="{4}/c_ops/c_ops_N{3}_Omega{5}_Delta{6}_run{2}".format(ang1,ang2,run_number,N, path_to_save_file, Omega, Delta)


name_of_file_r ="{4}positions/positions_N{3}_Omega{5}_Delta{6}_run{2}".format(ang1,ang2,run_number,N, path_to_save_file, Omega, Delta)



save_params_to_file(variables_string, filename)



np.savetxt(name_of_file_time, [end - start] ) 

np.save(name_of_file, [Beta1D, Beta2D, t_span])
#save_rhoss_to_file(r, name_of_file_r)
print(name_of_file_r)

save_rhoss_to_file(r, name_of_file_r)


#fig, ax = plt.subplots()  
#ax.plot(taulist, np.real(g2_lig)   )
#fig.savefig("testinho.png")
#plt.show()


print("PROGRAM FINISHED.\n Total time: ", end - start) # Time

