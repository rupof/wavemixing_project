import numpy  as np
import matplotlib.pyplot as plt
from plots.multi_plots import *
import sys
from correlation import *
import traceback


fig, axs = plt.subplots(figsize = (10,6) ,sharex = True, sharey = True)


N = str(sys.argv[1])
Omega = str(float(sys.argv[2]))
Delta = str(float(sys.argv[3]))
DefaultInfo = f"N{N}_Omega{Omega}_Delta{Delta}_"
description = str(sys.argv[4])
rho_ss_parameter = "_" + str(sys.argv[5])
results_path = "../results/"
defaultangle = "25"

taulist = np.arange(-1,1,0.1)

#interaction_list = ["On", "Off"]
labels = []
averages = []
array_of_many_runs = []



try:    
    label_folder =  results_path+"cauchy_schwarz_" + DefaultInfo+description+defaultangle + rho_ss_parameter + "/"
    labels.append(label_folder) 
    paths_array = get_array_of_runs_files(label_folder)
    print(paths_array[0])
    averages.append(average_of_runs_files(label_folder))
    print(len(averages))

except Exception as e:
    print(traceback.format_exc())


at25_25 = averages[0]
axs.set_title(DefaultInfo+description+defaultangle )
axs.plot(at25_25[0], at25_25[1], "r--", -at25_25[0], at25_25[1], "r--" , label = f"Simulation, Int: On")   
    

    


general_name = results_path+DefaultInfo+description

plt.savefig(general_name + f"on_off_{defaultangle}_cs.png")

    
#plt.ylim(0,10)
#plt.savefig(general_name + "s/N7_far_limavg.png")








