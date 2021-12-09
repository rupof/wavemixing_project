import numpy  as np
import matplotlib.pyplot as plt
from plots.multi_plots import *
import sys
import traceback




angles = [str(25), str(90), str(155), "-"+str(25), "-"+str(90), str(205)]



######
Omega1, Delta1 = float(2), float(20) 
Omega2, Delta2 = float(1), float(0)
Omega3, Delta3 = float(0.02), float(0)


results_path = "../results/"
defaultangle = "25_"
get_time = True

#############################


N_list = [1,2,3,4,5,6,7]

C1 = [Omega1, Delta1]
C2 = [Omega2, Delta2]
C3 = [Omega3, Delta3]

C_list = [C1,C2,C3]

b0_list = [0.1,3,5]
##################


def get_Nxtime_for_a_configuration(Omega, Delta, description):
    """
each array has 2 times
    """
    at_time25_25 = []
    at_time25_90 = []
    at_time25_155 = []
    at_time25_m25 = []
    at_time25_m90 = []
    at_time25_205 = []


    time_for_angle_and_N = [at_time25_25, at_time25_90, at_time25_155, at_time25_m25, at_time25_m90, at_time25_205]
    



    for N in range(1,len(N_list)+1):
        DefaultInfo = f"N{N}_Omega{Omega}_Delta{Delta}_"
        g2_by_angle, g2_time = get_array_of_many_runs_usual_conditions(N, Omega, Delta, DefaultInfo, description, results_path, defaultangle, get_time)
        try:
            at_time25_25.append(average_of_array_arrays(g2_time[0]))
        except:
            pass
        try: 
            at_time25_90.append(average_of_array_arrays(g2_time[1]))
        except:
            pass 
        try:
            at_time25_155.append(average_of_array_arrays(g2_time[2]))
        except:
            pass
        try:
            at_time25_m25.append(average_of_array_arrays(g2_time[3]))
        except:
            pass
        try:
            at_time25_m90.append(average_of_array_arrays(g2_time[4]))
        except:
            pass
        try:
            at_time25_205.append(average_of_array_arrays(g2_time[5]))
        except:
            pass



    return np.array(time_for_angle_and_N, dtype=object) 
        




def plot_time_in_axis_for_givenCandDescription(angle, C, description,ax_i ):
    time_for_angle_and_N  = get_Nxtime_for_a_configuration(*C,description )
    i = angle
    try:     
        
        total_time_ss = (np.array(time_for_angle_and_N[i]).T)[0]
        total_time_correlation =  (np.array(time_for_angle_and_N[i]).T)[1]

        Interaction = description[-3:-1]   
        print(Interaction)
        #ax_i.scatter(N_list, total_time_ss, marker="^", label = r"$\rho_{ss}$"+angle_label ) 
        #ax_i.scatter(N_list, total_time_correlation,marker= "v", label = r"$g^2(\tau)$"+angle_label) 

        ax_i.set_title(f"Omega, Delta = {C}")
        ax_i.set_ylabel(description[:6])
        
        ax_i.scatter(N_list, total_time_correlation+total_time_ss, label = Interaction)
        ax_i.set_yscale("log")
        ax_i.grid(True)


        ax_i.legend()
    
    except Exception as e: 
        print(traceback.format_exc())
        pass



def plot_as_function_of_b0_and_c(angle):
    for j, Ci in enumerate(C_list):
        for k, b0 in enumerate(b0_list):
            Description_On = f"b0_{b0}_V_Int_On_"
            Description_Off = f"b0_{b0}_V_Int_Off_"
            plot_time_in_axis_for_givenCandDescription(angle, Ci, Description_On, axs[j][k])
            plot_time_in_axis_for_givenCandDescription(angle, Ci, Description_Off, axs[j][k])



number_angles = [0,1,2,3,4,5]

for l, th in enumerate(angles):
    fig, axs = plt.subplots(3, 3, figsize = (10,6) ,sharex = True, sharey = True)
    plt.suptitle(th)

    plot_as_function_of_b0_and_c(l)
    plt.savefig(f"../results/g2_time_theta_{th}" ,dpi = 300)
















