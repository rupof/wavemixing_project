import numpy  as np
import matplotlib.pyplot as plt
from file_manager.visualization_preparation_tools import *
from correlation.second_order_correlation import *
import sys

fig, axs = plt.subplots(2, 3, figsize = (10,6) ,sharex = True, sharey = True)

axs[0, 0].set_title( r"$ \theta_1 = {0} $ $  \theta_2 = {1} $".format(25,25))
axs[1, 0].set_title( r"$ \theta_1 = {0}  $ $ \theta_2 = {1} $".format(25,-25))
axs[0, 1].set_title( r"$ \theta_1 = {0} $ $ \theta_2 = {1} $".format(25,90))
axs[1, 1].set_title( r"$ \theta_1 = {0}  $ $ \theta_2 = {1} $ ".format(25,-90))
axs[1, 2].set_title( r"$ \theta_1 = {0}  $ $ \theta_2 = {1} $ ".format(25,205))
axs[0, 2].set_title( r"$ \theta_1 = {0}  $ $ \theta_2 = {1} $ ".format(25,155))



angles = [str(25), str(90), str(155), "-"+str(25), "-"+str(90), str(205)]

N = str(sys.argv[1])
Omega = str(float(sys.argv[2]))
Delta = str(float(sys.argv[3]))
DefaultInfo = f"g2_N{N}_Omega{Omega}_Delta{Delta}_"
description = str(sys.argv[4])
results_path = "../results/"
defaultangle = "25_"
rho_ss_parameter = "_" + str(sys.argv[5])
taulist = np.arange(-1,1,0.01)



labels = []
array_of_many_runs = []


def get_list_organized_by_pairs(array_of_many_runs):
    pairs = []    
    for i in range(len(array_of_many_runs)):
        #print(i,i+1)    
        try:
            x0 = array_of_many_runs[i][0]
            y0 = array_of_many_runs[i][1]
            pairs.append(x0)
            pairs.append(y0)
        except:
            print(f"element {i}+1 does not exit")
    return pairs



for i, angle in enumerate(angles):
  #  try:
        
        label = results_path+DefaultInfo+description+defaultangle +angle+rho_ss_parameter+"/"
        labels.append(label)
        paths_array = get_array_of_runs_files(label)

        
        array_of_many_runs.append(get_array_of_numpy_runs(paths_array))

        




at25_25 = get_list_organized_by_pairs(array_of_many_runs[0])
at25_90 =  get_list_organized_by_pairs(array_of_many_runs[1])
at25_155 = get_list_organized_by_pairs(array_of_many_runs[2])
at25_m25 = get_list_organized_by_pairs(array_of_many_runs[3])
at25_m90 = get_list_organized_by_pairs(array_of_many_runs[4])
at25_205 = get_list_organized_by_pairs(array_of_many_runs[5])



axs[0, 0].plot(*at25_25 )
axs[1, 0].plot(*at25_m25)
axs[0, 1].plot(*at25_90)
axs[1, 1].plot(*at25_m90)
axs[1, 2].plot(*at25_205)
axs[0, 2].plot(*at25_155)


g12 = second_order_correlation_opposite_directions_interaction_off_araujo(taulist, float(Delta))

axs[1,2].plot(taulist, g12, label = "Theory")


#axs[0, 3].plot(at25_m90[0], at25_m90[1], label = r"$ \theta_1 = {0}  $ $ \theta_2 = {1} $ ".format(25,-90))




for i in range(len(axs)):
    for j in range(len(axs[i])):
        axs[i,j].legend()
    

general_name = results_path+DefaultInfo+description
    
plt.savefig(general_name + "all.png")
    
plt.ylim(0,10)
plt.savefig(general_name + "all_lim.png")








