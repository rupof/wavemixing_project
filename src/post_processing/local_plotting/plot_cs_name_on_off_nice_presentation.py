import numpy  as np
import matplotlib.pyplot as plt
from file_manager.visualization_preparation_tools import *
import sys
from correlation import *
import traceback

params = {'legend.fontsize': 'x-large',
          'figure.figsize': (15, 5),
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}

fig, axs = plt.subplots(figsize = (7,4) ,sharex = True, sharey = True)


N = str(sys.argv[1])
Omega = str(float(sys.argv[2]))
Delta = str(float(sys.argv[3]))
DefaultInfo = f"N{N}_Omega{Omega}_Delta{Delta}_"
description = str(sys.argv[4])
rho_ss_parameter = "_" + str(sys.argv[5])
results_path = "../results/"
defaultangle = "25"
b0 = 0.1
taulist = np.arange(-1,1,0.1)

#interaction_list = ["On", "Off"]
labels = []
averages = []
array_of_many_runs = []
geometric = True


try:    
    label_folder =  results_path+"cauchy_schwarz_" + DefaultInfo+description+defaultangle + rho_ss_parameter + "/"
    labels.append(label_folder) 
    paths_array = get_array_of_runs_files(label_folder)
    print(paths_array[0])
    averages.append(average_of_runs_files(label_folder, geometric))
    print(len(averages))

except Exception as e:
    print(traceback.format_exc())


at25_25 = averages[0]

#axs.set_title(DefaultInfo+description+defaultangle )
#axs.set_title("Cauchy-Schwartz Inequality for "+ f"$b_0 = {b0}, \Omega = {Omega}, \Delta = {Delta}$")
axs.plot(-at25_25[0]*26, at25_25[1], "r--",  linewidth=3  , label = f"Simulation: Interaction on")   
axs.plot(at25_25[0]*26, at25_25[1], "r--",  linewidth=3 )   
    

labels = []
averages = []
array_of_many_runs = []

try:    
    label_folder =  results_path+"cauchy_schwarz_" + DefaultInfo+description.replace("On","Off",1)+defaultangle + rho_ss_parameter + "/"
    labels.append(label_folder) 
    paths_array = get_array_of_runs_files(label_folder)
    averages.append(average_of_runs_files(label_folder, geometric))

except Exception as e:
    print(traceback.format_exc())



at25_25 = averages[0]

#axs.set_title(DefaultInfo+description+defaultangle )
axs.plot(-at25_25[0]*26, at25_25[1], "b--" , linewidth=3 ,  label = f"Simulation: Interaction off")   
axs.plot(at25_25[0]*26, at25_25[1], "b--", linewidth=3)   
#fig.suptitle(DefaultInfo+description )
plt.xlabel(r"$\tau$ [ns]", fontsize = 18)
plt.ylabel(r"R($\tau$)", fontsize = 18)


plt.legend()

#g12 = second_order_correlation_opposite_directions_interaction_off_araujo(taulist, float(Delta))

#axs[1,2].plot(taulist, g12, label = "Theory")


#for i in range(len(axs)):
#    for j in range(len(axs[i])):
#        axs[i,j].legend(loc = "upper left")


    


general_name = results_path+DefaultInfo+description

plt.savefig(general_name + f"on_off_{defaultangle}_cs.png",dpi = 300, bbox_inches="tight")

    
#plt.ylim(0,10)
#plt.savefig(general_name + "s/N7_far_limavg.png")








