import numpy  as np
import matplotlib.pyplot as plt
from plots.multi_plots import *
import sys
from correlation import *
import traceback


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
rho_ss_parameter = "_" + str(sys.argv[5])
results_path = "../results/"
defaultangle = "25_"

taulist = np.arange(-1,1,0.1)

#interaction_list = ["On", "Off"]
labels = []
averages = []
array_of_many_runs = []



for i, angle in enumerate(angles):
    try:    
        label = results_path+DefaultInfo+description+defaultangle +angle+ rho_ss_parameter + "/"
        labels.append(label)
        print(label)
        paths_array = get_array_of_runs_files(label)
        
        averages.append(average_of_runs_files(label))
        #print(averages[0][0])
        array_of_many_runs.append(get_array_of_numpy_runs(paths_array))
        print("blable")
    except:
        print(traceback.format_exc())


print("antes") 
at25_25 = averages[0]
at25_90 = averages[1]
at25_155 = averages[2]
at25_m25 = averages[3]
at25_m90 = averages[4]
at25_205 = averages[5]
print("depois")

ats = [at25_25, at25_90, at25_155, at25_m25, at25_m90, at25_205]



counter = 0
for i in range(2):
    for j in range(3):
        #print(i,j)
        #print(counter)
        axs[i, j].plot(ats[counter][0], ats[counter][1], label = "Int = On", c = "blue" )
        #axs[i, j].plot(-ats[counter][0], ats[counter][1], c = "gray" )
        counter += 1
    

labels = []
averages = []
array_of_many_runs = []



for i, angle in enumerate(angles):
    try:
        label = results_path+DefaultInfo + description.replace("On","Off",1)+defaultangle +angle+ rho_ss_parameter + "/"
        print(label)
        labels.append(label)
        paths_array = get_array_of_runs_files(label)

        averages.append(average_of_runs_files(label))
        
        array_of_many_runs.append(get_array_of_numpy_runs(paths_array))
    except:
        print(f"Not found: {label}")


at25_25 = averages[0]
at25_90 = averages[1]
at25_155 = averages[2]
at25_m25 = averages[3]
at25_m90 = averages[4]
at25_205 = averages[5]

ats = [at25_25, at25_90, at25_155, at25_m25, at25_m90, at25_205]


fig.suptitle(DefaultInfo+description )

counter = 0
for i in range(2):
    for j in range(3):
        print(i,j)
        #print(counter)
        axs[i, j].plot(ats[counter][0], ats[counter][1], label = "Int = Off", c = "gray" )
        #axs[i, j].plot(-ats[counter][0], ats[counter][1], c = "gray" )
        counter += 1



plt.legend()

#g12 = second_order_correlation_opposite_directions_interaction_off_araujo(taulist, float(Delta))

#axs[1,2].plot(taulist, g12, label = "Theory")


#for i in range(len(axs)):
#    for j in range(len(axs[i])):
#        axs[i,j].legend(loc = "upper left")


general_name = results_path+DefaultInfo+description
    
plt.savefig(general_name + "on_off" +"avg.png")
    
#plt.ylim(0,10)
#plt.savefig(general_name + "s/N7_far_limavg.png")








