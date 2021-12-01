import numpy  as np
import matplotlib.pyplot as plt
from plots.multi_plots import *
import sys
import traceback
import itertools



angles = [str(25), str(90), str(155), "-"+str(25), "-"+str(90), str(205)]



######
Omega1, Delta1 = float(2), float(20) 
Omega2, Delta2 = float(1), float(0)
Omega3, Delta3 = float(0.02), float(0)


results_path = "../results/"
defaultangle = "25_"
get_time = True

#############################


#N_list = [1,2,3,4,5,6,7,8]
N_list = [1,2,3,4,5,6]

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
        




def plot_time_in_axis_for_givenCandDescription(angle, C, description,ax_i, rho_ss_parameter = None ):
    time_for_angle_and_N  = get_Nxtime_for_a_configuration(*C,description )
    i = angle
    marker = itertools.cycle(('o', 'v', '^', '<', '>', 's', '8', 'p')) 
    try:    

       # color = next(ax_i._get_lines.prop_cycler)['color']

        total_time_ss = (np.array(time_for_angle_and_N[i]).T)[0]
        total_time_correlation =  (np.array(time_for_angle_and_N[i]).T)[1]

        Interaction = description[-3:-1]   
        print(Interaction)

        ax_i.set_title(f"Omega, Delta = {C}")
        ax_i.set_ylabel( "t [minutes]")
        
        ax_i.scatter(N_list, total_time_ss/60,marker= next(marker), label = r"$\rho_{ss} $"+ f"{rho_ss_parameter}")
        ax_i.scatter(N_list, total_time_correlation/60,marker= next(marker), label = r"$g^{(2)}(\tau)$" + f"{rho_ss_parameter}")
        ax_i.scatter(N_list, (total_time_correlation+total_time_ss)/60, marker=next(marker),  label = "total" + f"{rho_ss_parameter}")

        
        
        ax_i.grid(True)
        ax_i.set_yscale('log')

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

fig, axs = plt.subplots(1,1, figsize = (10,6) ,sharex = True, sharey = True)
th = number_angles[0]
angle = th
C = C1
description = "b0_0.1_V_Int_On_"
ax_i = axs
axs.set_ylabel("t [minutos]")
plt.suptitle(description + "25:" + angles[th])
plot_time_in_axis_for_givenCandDescription(angle, C, description,ax_i )



rho_ss_parameter_list = ["iterative-gmres", "manual", "svd", "eigen", "power" ]
for rho_ss_parameter in rho_ss_parameter_list:
    description = "b0_0.1_V_Int_On_"
    description += f"{rho_ss_parameter}"
    plot_time_in_axis_for_givenCandDescription(angle, C, description,ax_i, rho_ss_parameter )






###############################################















plt.savefig(f"../results/g2_time_theta_{th}_{description}.png" ,dpi = 300)






























