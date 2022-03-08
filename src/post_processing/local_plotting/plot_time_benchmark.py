import numpy  as np
import matplotlib.pyplot as plt
from file_manager.visualization_preparation_tools import *
import sys
import traceback




#angles = [str(25), str(90), str(155), "-"+str(25), "-"+str(90), str(205)]



######
#Omega1, Delta1 = float(2), float(20) 
#Omega2, Delta2 = float(1), float(0)
Omega3, Delta3 = float(0.05), float(0)


results_path = "../results/"
defaultangle = "25_"
get_time = True

#############################


N_list = [12, 20,25,30,40,42,44,50,60,70,80]

#C1 = [Omega1, Delta1]
#C2 = [Omega2, Delta2]
C3 = [Omega3, Delta3]

C_list = [C3]

b0_list = [0.1,3]
##################

#N50_Omega0.05_Delyta0.0_b0_0.1_S_Int_On_direct


def get_Nxtime_for_a_configuration(Omega, Delta, description):
    """
each array has 2 times
    """
    at_time_total = []
    at_time_ODE = []
    at_time_g2 = []


    time_for_operation = [at_time_total, at_time_ODE, at_time_g2]
    
    for N in N_list:
        DefaultInfo = f"N{N}_Omega{Omega}_Delta{Delta}_"
        g2_by_angle, g2_time = get_array_of_many_runs_usual_conditions(N, Omega, Delta, DefaultInfo, description, results_path, defaultangle, get_time, no_angle=True)
        try:
            at_time_total.append(average_of_array_arrays(g2_time[0]))
            at_time_ODE.append(average_of_array_arrays(g2_time[1]))
            at_time_g2.append(average_of_array_arrays(g2_time[2]))
        except:
            pass



    return np.array(time_for_operation, dtype=object) 
        




def plot_time_in_axis_for_givenCandDescription( C, description,ax_i ):
    time_for_angle_and_N  = get_Nxtime_for_a_configuration(*C,description )
    try:     
        print(time_for_angle_and_N)
        total_time = (np.array(time_for_angle_and_N[0]).T)[0]/60
        total_time_ODE =  (np.array(time_for_angle_and_N[0]).T)[1]/60
        total_time_g2 = (np.array(time_for_angle_and_N[0]).T)[2]/60
        
        print(len(total_time))
        print(len(N_list))

        ax_i.scatter(N_list, total_time, marker="^", label = r"Total time" ) 
        ax_i.scatter(N_list, total_time_ODE,marker= "v", label = r"Solving ODE") 

        ax_i.set_title(f"Omega, Delta = {C}")
        ax_i.set_ylabel("t(min)")
        ax_i.set_xlabel("N")        
        ax_i.scatter(N_list, total_time_g2, label = r"$g^{(2)}(0)$ by $\theta$ from ODE")
        ax_i.set_yscale("log")
        ax_i.grid(True)


        ax_i.legend()
    
    except Exception as e: 
        print(traceback.format_exc())
        pass




fig, axs = plt.subplots(1, 1, figsize = (10,6) ,sharex = True, sharey = True)
#plt.suptitle(th)
description = "b0_0.1_S_Int_On_direct"

plot_time_in_axis_for_givenCandDescription( C3, description,axs )
plt.savefig(f"../results/time_g2zero_theta" ,dpi = 300)
















