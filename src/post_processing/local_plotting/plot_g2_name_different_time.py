import numpy  as np
import matplotlib.pyplot as plt
from file_manager.visualization_preparation_tools import *
import sys
import traceback

import matplotlib as mpl
mpl.rcParams['lines.markersize']= 5
#mpl.rcParams["lines.markevery"]=5

fig, axs = plt.subplots(2, 3, figsize = (10,6) ,sharex = True, sharey = True)


markers=[".",",","o","v","^","<",">","1","2","3","4","8","s","p","P","*","h","H","+","x","X","D","d","|","_",0,1,2,3,4,5,6,7,8,9,10,11]


angles = [str(25), str(90), str(155), "-"+str(25), "-"+str(90), str(205)]

b0 = sys.argv[1]
N = 7
Omega = 1.0
Delta = 0.0 
DefaultInfo = f"N{N}_Omega{Omega}_Delta{Delta}_"
description = f"b0_{b0}_V_Int_On_"
results_path = "../results/"
defaultangle = "25_"
rho_ss_parameter = "_manual_"
t_list = [0.1, 0.5, 1, 3, 10]
t_list_T = [0.1, 0.25, 0.5, 1, 3, 10, 50, 100, 500]




labels = []
averages = []
array_of_many_runs = []



axs[0, 0].set_title( r"$ \theta_1 = {0} $ $  \theta_2 = {1} $".format(25,25))
axs[1, 0].set_title( r"$ \theta_1 = {0}  $ $ \theta_2 = {1} $".format(25,-25))
axs[0, 1].set_title( r"$ \theta_1 = {0} $ $ \theta_2 = {1} $".format(25,90))
axs[1, 1].set_title( r"$ \theta_1 = {0}  $ $ \theta_2 = {1} $ ".format(25,-90))
axs[1, 2].set_title( r"$ \theta_1 = {0}  $ $ \theta_2 = {1} $ ".format(25,205))
axs[0, 2].set_title( r"$ \theta_1 = {0}  $ $ \theta_2 = {1} $ ".format(25,155))




for t_i, t in enumerate(t_list_T[:]):
    labels = []
    averages = []
    for i, angle in enumerate(angles):
      #  try:
        try: 
            label_folder = results_path+DefaultInfo+description+defaultangle +angle+ rho_ss_parameter+str(float(t)) + "/"
            #label = results_path+DefaultInfo+description+defaultangle +angle 
            labels.append(label_folder)
            
            paths_array = get_array_of_runs_files(label_folder)

            averages.append(average_of_runs_files(label_folder))
            
            array_of_many_runs.append(get_array_of_numpy_runs(paths_array))
        except Exception as e:
            print(t, angle)
#            print(e)
            print(traceback.format_exc())
           # print(sys.exc_info()[2])

    print(averages[0])        
    at25_25 = averages[0]
    at25_90 = averages[1]
    at25_155 = averages[2]
    at25_m25 = averages[3]
    at25_m90 = averages[4]
    at25_205 = averages[5]


    axs[0, 0].plot(at25_25[0], at25_25[1], label = f"t = {t}")
    axs[1, 0].plot(at25_m25[0], at25_m25[1], label = f"t = {t}" )
    axs[0, 1].plot(at25_90[0], at25_90[1],  label = f"t = {t}" )
    axs[1, 1].plot(at25_m90[0], at25_m90[1], label = f"t = {t}" )

    axs[1, 2].plot(at25_205[0], at25_205[1],  label = f"t = {t}" )
    axs[0, 2].plot(at25_155[0], at25_155[1], label = f"t = {t}")


    for i in range(len(axs)):
        for j in range(len(axs[i])):
            #axs[i,j].legend()
            handles, labels = axs[i,j].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper left')


general_name = results_path+DefaultInfo+description

plt.savefig(general_name + "manual_convergence.png")


plt.ylim(0,10)
plt.savefig(general_name + "lim_manual_convergence.png")


plt.show()

    
#plt.ylim(0,10)
#plt.savefig(general_name + "s/N7_far_limavg.png")








