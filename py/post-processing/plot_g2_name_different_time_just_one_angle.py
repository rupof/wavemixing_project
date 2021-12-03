import numpy  as np
import matplotlib.pyplot as plt
from plots.multi_plots import *
import sys
import traceback

fig, axs = plt.subplots(1, 1, figsize = (10,6) ,sharex = True, sharey = True)


b0_input = str(sys.argv[1])
N = 7
Omega = 0.02
Delta = 0.0 
DefaultInfo = f"N{N}_Omega{Omega}_Delta{Delta}_"
description = f"b0_{b0_input}_V_Int_On_"
results_path = "../results/"
defaultangle = "25_"
rho_ss_parameter = "_manual_"
t_list = [0.1, 0.5, 1, 3, 10]
t_list_T = [0.1, 0.5, 1, 3, 10, 50, 100 ]



labels = []
averages = []
array_of_many_runs = []


angle_input =str(-90)
angle = angle_input 
 

for  i, t in enumerate(t_list_T[:]):
      #  try:
    try: 
        label_folder = results_path+DefaultInfo+description+defaultangle +angle+ rho_ss_parameter+str(float(t)) + "/"
        #label = results_path+DefaultInfo+description+defaultangle +angle 
        labels.append(label_folder)
        
        paths_array = get_array_of_runs_files(label_folder)

        averages.append(average_of_runs_files(label_folder))
        
    except Exception as e:
        print(t, angle)
#            print(e)
        print(traceback.format_exc())
        continue
       # print(sys.exc_info()[2])
    print(averages)
    at25_25 = averages[i]
    axs.set_title(DefaultInfo+description+defaultangle +angle)
    axs.plot(at25_25[0], at25_25[1], label = f"t = {t}")   
    axs.legend()


general_name = results_path+DefaultInfo+description
    
plt.savefig(general_name + f"25_{angle}_manual_convergence.png")
    
#plt.ylim(0,10)
#plt.savefig(general_name + "s/N7_far_limavg.png")








