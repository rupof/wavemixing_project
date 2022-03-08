import numpy  as np
import matplotlib.pyplot as plt
from file_manager.visualization_preparation_tools import *
import sys
import traceback
from correlation import *


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
DefaultInfo = f"N{N}_Omega{Omega}_Delta{Delta}_"

geometric = False
rho_ss_parameter = "_direct"
results_path = "../results/"
defaultangle = "25_"


b0_list = [float(0.10)*i for i in range(1,101)]

taulist = np.arange(-1,1,0.1)


labels = []
averages = []
array_of_many_runs = []

def get_array_of_g2zero(description):
    try:  
         labels = []
         averages = []
         
         label_folder =  results_path+"g2zero_" + DefaultInfo+description + rho_ss_parameter + "/"
         labels.append(label_folder) 
         paths_array = get_array_of_runs_files(label_folder)[:150]
         #print(paths_array[0])
         runs_txt = get_array_of_numpy_runs(paths_array)
         averages.append(average_of_runs_files(label_folder[:], geometric))
         #print(len(averages))
    except Exception as e:
         print(traceback.format_exc())
    return averages

at25_25 = [] #averages[0]
at25_90 = [] #averages[1]
at25_155 = [] #averages[2]
at25_m25 = [] #verages[3]
at25_m90 = [] #averages[4]
at25_205 = [] #verages[5]

b0_plot = []
for b0 in b0_list:
    try:
        description = f"b0_{b0:.2f}_S_Int_On_changingOD_t01"    
        if b0 <1:
            b0_str = f"{b0:.2f}"[1:]
            description = f"b0_{b0_str}_S_Int_On_changingOD_t01"    
        averages_of_arrays = get_array_of_g2zero(description)   
        averages = averages_of_arrays[0][1]
        print(f"{b0:.2f}",(averages))

        if max(averages) > 200:
            print(b0, "esquito")
            continue
        b0_plot.append(b0)
        at25_25.append(averages[0])
        at25_90.append(averages[1])
        at25_155.append(averages[2])
        at25_m25.append(averages[3])
        at25_m90.append(averages[4])
        at25_205.append(averages[5])
    except Exception as e:
        print(traceback.format_exc())
        #break 


print(len(averages[:]) )
ats = [at25_25, at25_90, at25_155, at25_m25, at25_m90, at25_205]


        #fig.suptitle(DefaultInfo+description )
counter = 0
for i in range(2):
    for j in range(3):
                #print(i,j)
                #print(counter)
        axs[i, j].plot(b0_plot, ats[counter], c = "gray" )
        axs[i,j].set_xlabel("$b_0$")
        axs[i,j].set_ylabel("$g^{(2)}(0)$")


                #axs[i, j].plot(-ats[counter][0], ats[counter][1], c = "gray" )
        counter += 1



#g12 = second_order_correlation_opposite_directions_interaction_off_araujo(taulist, float(Delta))

#axs[1,2].plot(taulist, g12, label = "Theory")


#for i in range(len(axs)):
#    for j in range(len(axs[i])):
#        axs[i,j].legend(loc = "upper left")


general_name = results_path+DefaultInfo+description
    
plt.savefig(general_name + "avg.png")
    
#plt.ylim(0,10)
#plt.savefig(general_name + "s/N7_far_limavg.png")








