import numpy  as np
import matplotlib.pyplot as plt
from file_manager.visualization_preparation_tools import *
import sys
import traceback

fig, axs = plt.subplots(1, 1, figsize = (10,6) ,sharex = True, sharey = True)


b0_input = str(sys.argv[1])
N = 7
Omega = 1.0
Delta = 0.0 
DefaultInfo = f"N{N}_Omega{Omega}_Delta{Delta}_"
description = f"b0_{b0_input}_V_Int_On_"
results_path = "../results/"
defaultangle = "25_"
rho_ss_parameter = "_manual_"
#t_list = [0.1, 0.5, 1, 3, 10]
t_list_T = [0.1, 0.25, 0.5, 1, 3, 10, 50, 100, 500]

n = 30
markers=[".",",","o","v","^","<",">","1","2","3","4","8","s","p","P","*","h","H","+","x","X","D","d","|","_",0,1,2,3,4,5,6,7,8,9,10,11
]


labels = []
averages = []
array_of_many_runs = []


angle_input =str(-25)
angle = angle_input 


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


for  i, t in enumerate(t_list_T[:]):
      #  try:
    #labels = []
   # averages = []

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
        continue
       # print(sys.exc_info()[2])
    at25_25 = averages[i]
    axs.set_title(DefaultInfo+description+defaultangle +angle)
    axs.plot(at25_25[0], at25_25[1], label = f"avg: t = {t}")  

    at25 = get_list_organized_by_pairs(array_of_many_runs[0])
    print(len(at25))
    for i in range(0,int(len(at25)), 2):
        axs.plot(at25[i], at25[i+1], marker = markers[i], label = f"run {i/2}")
    

    axs.legend()




















general_name = results_path+DefaultInfo+description
    
plt.savefig(general_name + f"25_{angle}_manual_convergence.png")
    
#plt.ylim(0,10)
#plt.savefig(general_name + "s/N7_far_limavg.png")








