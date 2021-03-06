import matplotlib.pyplot as plt
import numpy as np
from qutip import *
from timeit import default_timer as timer

from file_manager.visualization_preparation_tools import get_rho_ss_list
from helper_functions.interaction_preparation import *
from helper_functions.operators import *
from helper_functions.other import * 
from hamiltonian.hamiltonian_builder import *
from hamiltonian.different_waves import *
from correlation.second_order_correlation import *
from file_manager import get_path_to_save_files, get_new_run_number_txt, save_params_to_file, save_rhoss_to_file

import traceback
import sys


"""Given some initial parameters this scripts obtains cs, from local results (rho_ss) """

def get_cs_for_a_rho_ss(ang1,ang2, N, useb0, b0, kd, description, interaction, Omega, Delta, rho_ss_parameter, tmax, rho_ss, r ):

    taulist = np.linspace(0,1, 100) 
    Gamma = 1
    nhat = 0

    print(f"ang1 = {ang1}")
    print(f"ang2 = {ang2}")#useless
    print(f"N = {N}")
    print(f"useb0 = {useb0}")
    kd = None
    exc_radius = None
    print(f"b0 = {b0}, description = {description}")
    print(f"interaction = {interaction}")
    print(f"Omega = {Omega}")
    print(f"Delta = {Delta}")
    print(f"rho_ss_parameter = {rho_ss_parameter}")
    print(f"tmax = {tmax}")
    print(f"r size: {len(r)}")




    psi0 = tensor([ket("1") for i in range(N) ])
    wave_mixing = True
    scalar = False
    description += f'_{ang1}_{rho_ss_parameter}'

    if tmax != 0:
        description += f'_{tmax}'



    H, c_ops, GTensor,M, GammaSR, DeltaSR, Omega, SR_state, r = system_spec_N(Gamma, N, kd = kd, b0 = b0, exc_radius = exc_radius , Delta = Delta, Omega = Omega, wave_mixing = wave_mixing, scalar = scalar, interaction=interaction, r = r)
   

    rho_ss_results = Qobj(rho_ss, dims=H.dims)
    
    #print(f"--------{interaction}-----------\n debug")
    #print("Hdim = \n  ", H)
    #print("c_ops = \n  ", c_ops[1])
    #print("rho_ss = \n ", rho_ss_results)

    print("-----------------------end")

    R, rho_ss= cauchy_schwarz(H, nhat, r, ang1, taulist, c_ops, N, faseglobal = False, rho_ss = rho_ss_results, rho_ss_parameter = rho_ss_parameter, tmax = tmax)

  #  print(rho_ss == rho_ss_results, "rho_ss equal to input (we expect True)" )


    variables = r"$ \Gamma={0}, \Omega={1} \Gamma, \Delta = {2} , kd = {3}, N = {4}, b0 = {5} $".format(Gamma,Omega, Delta, kd, N, b0)

    variables_string = "Gamma={0} \nOmega={1}*Gamma \nDelta = {2} \nkd = {3} \nN = {4}  \nb0 = {5}\nscalar = {6}, interaction = {7} ".format(Gamma,Omega, Delta, kd, N, b0, scalar , interaction)



  #  end = timer()

    #Saving files!

        
    path_to_save_file = get_path_to_save_files(N, Omega, Delta,  description, extra_folder_name="cauchy_schwarz_", extra_path = "") #Change to add ../
    filename ="{4}/angulo{0}_N{3}_Omega{5}_Delta{6}_run".format(ang1,ang2,0,N,path_to_save_file, Omega, Delta) 
    run_number = get_new_run_number_txt(filename)
    name_of_file =  "{4}/angulo{0}_N{3}_Omega{5}_Delta{6}_run{2}.txt".format(ang1,ang2,run_number,N, path_to_save_file, Omega, Delta)
    name_of_file_time =  "{4}/time/time_angulo{0}_N{3}_Omega{5}_Delta{6}_run{2}.txt".format(ang1,ang2,run_number,N, path_to_save_file, Omega, Delta)
    name_of_file_r ="{4}/positions/positions_N{3}_Omega{5}_Delta{6}_run{2}".format(ang1,ang2,run_number,N, path_to_save_file, Omega, Delta)

    save_params_to_file(variables_string, filename)


    np.savetxt(name_of_file, [taulist, R])
    save_rhoss_to_file(r, name_of_file_r)

    #np.savetxt(name_of_file_time, [total_time_ss, total_time_correlation] ) 

    #save_rhoss_to_file(rho_ss, name_of_file)
    #fig, ax = plt.subplots()  
    #ax.plot(taulist, np.real(g2_lig)   )
    #fig.savefig("testinho.png")
    #plt.show()


   # print(end - start) # Time

def get_cs_from_all_available_rho_ss(ang1, N, useb0, b0,kd, description, interaction, Omega, Delta, rho_ss_parameter, tmax):

    rho_ss_list, r_list = get_rho_ss_list(N, Omega, Delta, description, rho_ss_parameter= rho_ss_parameter, results_path="../results/")
    #print("rho_ss \n", rho_ss_list)

    #print("r \n", r_list)



    for index, rho_ss  in enumerate(rho_ss_list):
        try:
            r = r_list[index]
            get_cs_for_a_rho_ss(ang1, 0, N, useb0, b0, None, description, interaction, Omega, Delta, rho_ss_parameter, tmax, rho_ss, r) 
            print ("rho_ss index =", index)
        except Exception:
            print(traceback.format_exc())

            print("get_cs; error in run:", index)



