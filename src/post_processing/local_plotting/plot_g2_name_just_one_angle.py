import numpy  as np
import matplotlib.pyplot as plt
from file_manager.visualization_preparation_tools import *
import sys
import traceback
from correlation import *
from scipy.optimize import curve_fit

import warnings
warnings.filterwarnings("error")

fig, axs = plt.subplots(1, 1, figsize = (10,6) ,sharex = True, sharey = True)


######

### Interaction On
b0_input = str(sys.argv[1])
N = 7
Omega = 2.0
Delta = 20.0 
DefaultInfo = f"g2_N{N}_Omega{Omega}_Delta{Delta}_"
description = f"b0_{b0_input}_V_Int_On_fixed__"
descriptionOff = f"b0_{b0_input}_V_Int_Off_fixed__"
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
 

  #  try:
try: 
    label_folder = results_path+DefaultInfo+description+defaultangle +angle+ rho_ss_parameter + "/"
    labels.append(label_folder) 
    paths_array = get_array_of_runs_files(label_folder)
    averages.append(average_of_runs_files(label_folder))
    
    label_folder = results_path+DefaultInfo+descriptionOff+defaultangle +angle+ rho_ss_parameter + "/"
    labels.append(label_folder) 
    paths_array = get_array_of_runs_files(label_folder)
    averages.append(average_of_runs_files(label_folder))
     



except Exception as e:
#            print(e)
    print(traceback.format_exc())
    
   # print(sys.exc_info()[2])



at25_25 = averages[0]
axs.set_title(DefaultInfo+description+defaultangle +angle)
axs.plot(at25_25[0], at25_25[1], "r--", -at25_25[0], at25_25[1], "r--" , label = f"Simulation, Int: On")   


try:
    func = second_order_correlation_opposite_directions_interaction_on_empirical_araujo
    popt, pcov = curve_fit(func, at25_25[0], at25_25[1]) 
    plt.plot(taulist, func(taulist, *popt), 'r-', label='fit: Delta=%5.3f, f=%5.3f, chi=%5.3f' % tuple(popt))
except:
    print("ugly fit")
    pass



at25_25 = averages[1]
axs.set_title(DefaultInfo+description[:-1]+defaultangle +angle)
axs.plot(at25_25[0], at25_25[1], "b--" ,-at25_25[0], at25_25[1],"b--" , label = f"Simulation, Int: Off")   


#Curva Teo
g12 = second_order_correlation_opposite_directions_interaction_off_araujo(taulist, float(Delta))
axs.plot(taulist, g12, label = "Theory")

#Curva fitada

axs.legend()


general_name = results_path+DefaultInfo+description
    
plt.savefig(general_name + f"25_{angle}_manual_with_fit_comparison_mean.png")
    
#plt.ylim(0,10)
#plt.savefig(general_name + "s/N7_far_limavg.png")








