import numpy  as np
import matplotlib.pyplot as plt
from file_manager.visualization_preparation_tools import *
import sys
import traceback
from correlation import *
from scipy.optimize import curve_fit
from matplotlib import rc


import warnings
warnings.filterwarnings("error")

params = {'legend.fontsize': 'x-large',
          'figure.figsize': (15, 5),
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
plt.rcParams.update(params)


fig, axs = plt.subplots(1, 2, figsize = (10,6) ,sharex = True, sharey = True)

#rc('text', usetex=True)
######

### Interaction On
b0_input = str(sys.argv[6])
N = int(sys.argv[1])
Omega = float(sys.argv[2])
Delta = float(sys.argv[3])
DefaultInfo = f"g2_N{N}_Omega{Omega}_Delta{Delta}_"
description = str(sys.argv[4]) #f"b0_{b0_input}_S_Int_On_QRT_"
results_path = "../results/"
defaultangle = "25_"
rho_ss_parameter = "_direct"
#t_list = [0.1, 0.5, 1, 3, 10]
 
taulist = np.arange(-1,1, 0.01)


labels = []
averages = []
array_of_many_runs = []


angle_input =str(205)
angle = angle_input 
 
fig.suptitle(r"$g^{(2)}(\tau)$ " + f" b_0 = {b0_input}, Omega = {Omega}, Delta  = {Delta}  ")

  #  try:
try: 
    label_folder = results_path+DefaultInfo+description+defaultangle +angle+ rho_ss_parameter + "/"
    labels.append(label_folder) 
    paths_array = get_array_of_runs_files(label_folder)
    averages.append(average_of_runs_files(label_folder))




except Exception as e:
#            print(e)
    print(traceback.format_exc())
    
   # print(sys.exc_info()[2])



at25_25 = averages[0]
axs[0].set_title("g^{(2)}_{12}")
axs[0].plot(at25_25[0], at25_25[1], "r--" ,   linewidth=3 ,label = f"Simulation: Interaction on")   
axs[0].plot(-at25_25[0], at25_25[1], "r--" ,  linewidth=3 )   




############################################################################################

N = int(sys.argv[1])
Omega = float(sys.argv[2])
Delta = float(sys.argv[3])
DefaultInfo = f"g2_N{N}_Omega{Omega}_Delta{Delta}_"
description = str(sys.argv[4]) 

results_path = "../results/"
defaultangle = "25_"
rho_ss_parameter = "_direct"
#t_list = [0.1, 0.5, 1, 3, 10]

taulist = np.arange(-1,1, 0.01)


labels = []
averages = []
array_of_many_runs = []


angle_input =str(25)
angle = angle_input


  #  try:
try:
    label_folder = results_path+DefaultInfo+description+defaultangle +angle+ rho_ss_parameter + "/"
    labels.append(label_folder)
    paths_array = get_array_of_runs_files(label_folder)
    averages.append(average_of_runs_files(label_folder))




except Exception as e:
#            print(e)
    print(traceback.format_exc())

   # print(sys.exc_info()[2])



at25_25 = averages[0]
axs[1].set_title("g^{(2)}_{11}")
axs[1].plot(at25_25[0], at25_25[1], "r--" ,  linewidth=3 , label = f"")
axs[1].plot(-at25_25[0], at25_25[1], "r--",  linewidth=3  )





axs[1].set_xlabel(r"$\tau$")
axs[0].set_ylabel(r"$g^{(2)}(\tau)$")




axs[1].legend(loc='upper center', bbox_to_anchor=(0.5, -0.17),
          fancybox=True, shadow=True, ncol=1, prop={'size': 15})



general_name = results_path+DefaultInfo+description
    
plt.savefig(general_name + "nice_picture_two_angles" + f"25_{angle}.png", dpi = 300, bbox_inches="tight")
    
#plt.ylim(0,10)
#plt.savefig(general_name + "s/N7_far_limavg.png")








