import matplotlib.pyplot as plt
import numpy as np
from qutip import *
from timeit import default_timer as timer
from helper_functions.interaction_preparation import *
from helper_functions.operators import *
from helper_functions.other import * 
from hamiltonean_builder.hamiltonean_builder import *
from correlation.second_order_correlation import *
from file_manager import get_path_to_save_files, get_new_run_number_txt, save_params_to_file, save_rhoss_to_file

from plots.multi_plots import get_rho_ss_list
import traceback
import sys



"""Given some initial parameters this scripts obtains g2, from local results (rho_ss or Beta1D, Beta2D) """

def get_g2_for_a_rho_ss(ang1,ang2, N, useb0, b0, kd, description, interaction, Omega, Delta, rho_ss_parameter, tmax, rho_ss, r ):
    """
    Calculates g2 given ang1, ang2 and saves it. (Description to be improved...)

    """
    R1 = get_nhat_from_angle(ang1)
    R2 = get_nhat_from_angle(ang2)
    


    taulist = np.linspace(0,1, 100) 
    Gamma = 1
    nhat = 0

    print(f"ang1 = {ang1}")
    print(f"ang2 = {ang2}")
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
    description += f'_{int(ang1)}_{int(ang2)}_{rho_ss_parameter}'

    if tmax != 0:
        description += f'_{tmax}'




    H, c_ops, GTensor,M, GammaSR, DeltaSR, Omega, SR_state, r = system_spec_N(Gamma, N, kd = kd, b0 = b0, exc_radius = exc_radius , Delta = Delta, Omega = Omega, wave_mixing = wave_mixing, scalar = scalar, interaction=interaction, r = r)
    

    rho_ss_results = Qobj(rho_ss, dims=H.dims)

    g2_lig, rho_ss_out, total_time_ss, total_time_correlation  = g2_l(H, nhat, r,R1, R2, taulist, c_ops, N, faseglobal = 1, rho_ss = rho_ss_results, rho_ss_parameter = rho_ss_parameter, tmax = tmax)



    print(rho_ss_out == rho_ss_results, "rho_ss equal to input (we expect True)" )


    variables = r"$ \Gamma={0}, \Omega={1} \Gamma, \Delta = {2} , kd = {3}, N = {4}, b0 = {5} $".format(Gamma,Omega, Delta, kd, N, b0)

    variables_string = "Gamma={0} \nOmega={1}*Gamma \nDelta = {2} \nkd = {3} \nN = {4}  \nb0 = {5}\nscalar = {6}, interaction = {7} ".format(Gamma,Omega, Delta, kd, N, b0, scalar , interaction)

    ##################################################
    #Saving files and dealing with names
        
    path_to_save_file = get_path_to_save_files(N, Omega, Delta,  description, extra_folder_name="g2_", extra_path = "") #Change to add ../
    filename ="{4}/angulo{0}e{1}_N{3}_Omega{5}_Delta{6}_run".format(ang1,ang2,0,N,path_to_save_file, Omega, Delta) 
    run_number = get_new_run_number_txt(filename)
    name_of_file =  "{4}/angulo{0}e{1}_N{3}_Omega{5}_Delta{6}_run{2}.txt".format(ang1,ang2,run_number,N, path_to_save_file, Omega, Delta)
    name_of_file_time =  "{4}/time/time_angulo{0}e{1}_N{3}_Omega{5}_Delta{6}_run{2}.txt".format(ang1,ang2,run_number,N, path_to_save_file, Omega, Delta)

    name_of_file_r ="{4}/positions/positions_N{3}_Omega{5}_Delta{6}_run{2}".format(ang1,ang2,run_number,N, path_to_save_file, Omega, Delta)


    

    save_params_to_file(variables_string, filename)
    np.savetxt(name_of_file, [taulist, g2_lig])
    save_rhoss_to_file(r, name_of_file_r)
    
    
#np.savetxt(name_of_file_time, [total_time_ss, total_time_correlation] ) 

    #save_rhoss_to_file(rho_ss, name_of_file)
    #fig, ax = plt.subplots()  
    #ax.plot(taulist, np.real(g2_lig)   )
    #fig.savefig("testinho.png")
    #plt.show()


   # print(end - start) # Time

def get_g2_from_all_available_rho_ss(ang1,ang2, N, useb0, b0, kd, description, interaction, Omega, Delta, rho_ss_parameter, tmax  ):

    rho_ss_list, r_list,  = get_rho_ss_list(N, Omega, Delta, description, rho_ss_parameter= rho_ss_parameter, results_path="../results/")


    for index, rho_ss  in enumerate(rho_ss_list):
        try:
            r = r_list[index]
            get_g2_for_a_rho_ss(ang1,ang2, N, useb0, b0, kd, description, interaction, Omega, Delta, rho_ss_parameter, tmax, rho_ss,r  )
            print ("rho_ss index =", index)
        except Exception:
            print(traceback.format_exc())

            print("get_g2; error in run:", index)



def get_all_g2_zero_for_a_beta(r, Beta1D_list, Beta2D_list, N, useb0, b0, kd, description, interaction, Omega, Delta  ): 
    ang1 = 25
    scalar = True
    R1 = get_nhat_from_angle(ang1)
    
    ang2 = np.linspace(0, 360, 120)
    R2_list = [] 
    g2_zero = []
 
    for theta in ang2:
        R2_list.append(get_nhat_from_angle(theta))
        g2_zero.append(0)

    Gamma = 1
    nhat = 0
    
    for i in range(len(R2_list)):
        R2 = R2_list[i]
        g2_zero[i] = np.real(g2_of_zero_subspace_approach(r, R1, R2, Beta1D_list[-1], Beta2D_list[-1]))

    variables = r"$ \Gamma={0}, \Omega={1} \Gamma, \Delta = {2} , kd = {3}, N = {4}, b0 = {5} $".format(Gamma,Omega, Delta, kd, N, b0)

    variables_string = "Gamma={0} \nOmega={1}*Gamma \nDelta = {2} \nkd = {3} \nN = {4}  \nb0 = {5}\nscalar = {6}, interaction = {7} ".format(Gamma,Omega, Delta, kd, N, b0, scalar , interaction)

    ##################################################
    #Saving files and dealing with names

    path_to_save_file = get_path_to_save_files(N, Omega, Delta,  description, extra_folder_name="g2zero_", extra_path = "") #Change to add ../
    filename ="{4}/ODE_N{3}_Omega{5}_Delta{6}_run".format(ang1,ang2,0,N,path_to_save_file, Omega, Delta)
    run_number = get_new_run_number_txt(filename)
    name_of_file =  "{4}/ODE_N{3}_Omega{5}_Delta{6}_run{2}.txt".format(ang1,ang2,run_number,N, path_to_save_file, Omega, Delta)
    name_of_file_time =  "{4}/time/time_N{3}_Omega{5}_Delta{6}_run{2}.txt".format(ang1,ang2,run_number,N, path_to_save_file, Omega, Delta)

    name_of_file_r ="{4}/positions/positions_N{3}_Omega{5}_Delta{6}_run{2}".format(ang1,ang2,run_number,N, path_to_save_file, Omega, Delta)




    save_params_to_file(variables_string, filename)
    np.savetxt(name_of_file, [ang2, g2_zero])
    save_rhoss_to_file(r, name_of_file_r)
    return run_number

#np.savetxt(name_of_file_time, [total_time_ss, total_time_correlation] )

    #save_rhoss_to_file(rho_ss, name_of_file)
    #fig, ax = plt.subplots()
    #ax.plot(taulist, np.real(g2_lig)   )
    #fig.savefig("testinho.png")
    #plt.show()


   # print(end - start) # Time

def get_g2_zero_from_all_available_rho_ss(N, useb0, b0, kd, description, interaction, Omega, Delta, rho_ss_parameter, tmax  ):
    
    beta_list, r_list,  = get_rho_ss_list(N, Omega, Delta, description, rho_ss_parameter= rho_ss_parameter, results_path="../results/", get_beta = True)


    for index, beta  in enumerate(beta_list):
        try:
            Beta1D_list, Beta2D_list = beta[0], beta[1]
            r = r_list[index]
            get_all_g2_zero_for_a_beta(r, Beta1D_list, Beta2D_list, N, useb0, b0, kd, description, interaction, Omega, Delta  )
            print ("rho_ss index =", index)
        except Exception:
            print(traceback.format_exc())

            print("get_g2; error in run:", index)


