import numpy  as np
import matplotlib.pyplot as plt
from file_manager.visualization_preparation_tools import *
import sys
from correlation import *
import traceback


fig, axs = plt.subplots(figsize = (10,6) ,sharex = True, sharey = True)
#fig, axs = plt.subplots(figsize = (10,6),subplot_kw={'projection': 'polar'})


N = str(sys.argv[1])
Omega = str(float(sys.argv[2]))
Delta = str(float(sys.argv[3]))
DefaultInfo = f"N{N}_Omega{Omega}_Delta{Delta}_"
description = str(sys.argv[4])
rho_ss_parameter = "_" + str(sys.argv[5])
results_path = "../results/"
defaultangle = "25"
geometric = False

#interaction_list = ["On", "Off"]
labels = []
averages = []
array_of_many_runs = []



try:    
    label_folder =  results_path+"g2zero_" + DefaultInfo+description + rho_ss_parameter + "/"
    labels.append(label_folder) 
    paths_array = get_array_of_runs_files(label_folder)[:150]
    #print(paths_array[0])
    runs_txt = get_array_of_numpy_runs(paths_array)
    averages.append(average_of_runs_files(label_folder[:], geometric))
    print(len(averages))
except Exception as e:
    print(traceback.format_exc())


at25_25 = averages[0]
axs.set_title(DefaultInfo+description+defaultangle )
axs.plot(at25_25[0], at25_25[1], "r-s",   label = f"Average")   

convert_factor =1 # 3.1415/180
for i in range(len(runs_txt)):
    if (runs_txt[i][1]<0).any() == True :
        n = str(paths_array[i])[-6:-4]
        print(n)
        axs.plot(runs_txt[i][0]*convert_factor, runs_txt[i][1], label = f"Simulation {n} is negative")
        print(paths_array[i])
    else:
                
        #if np.max(runs_txt[i][1])>5:
        #    continue
        axs.plot(runs_txt[i][0]*convert_factor, runs_txt[i][1])
            
        pass
    
axs.axvline(25*convert_factor, linestyle = "--")
axs.axvline(205*convert_factor, linestyle = "--")


axs.legend(prop={'size': 10})



#axs.set_rmax(1000)

general_name = results_path+DefaultInfo+description

plt.savefig(general_name + f"polar_ODEint.png")
plt.show()
   
fig, axs = plt.subplots(figsize = (10,6),subplot_kw={'projection': 'polar'})


convert_factor =3.1415/180
at25_25 = averages[0]

for i in range(len(runs_txt)):
    #if max(runs_txt[i][1]) >= 5:
    #    continue
    #axs.scatter(runs_txt[i][0]*convert_factor, runs_txt[i][1])
    pass
axs.set_title(DefaultInfo+description+defaultangle )
axs.plot(at25_25[0]*convert_factor, at25_25[1],   label = f"Average")
axs.axvline(25*convert_factor, linestyle = "--")
axs.axvline(205*convert_factor, linestyle = "--")

plt.savefig(general_name + f"polar_circle_ODEint.png")


#plt.ylim(0,10)
#plt.savefig(general_name + "s/N7_far_limavg.png")








