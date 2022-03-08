import numpy  as np
import matplotlib.pyplot as plt
from file_manager.visualization_preparation_tools import *
import sys
import traceback
from correlation import *
from scipy.optimize import curve_fit
from matplotlib import rc

params = {'legend.fontsize': 'x-large',
          'figure.figsize': (15, 5),
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
plt.rcParams.update(params)
import warnings
warnings.filterwarnings("error")

fig, axs = plt.subplots(1, 1, figsize = (7,4) ,sharex = True, sharey = True)

#rc('text', usetex=True)
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
geometric = True
#t_list = [0.1, 0.5, 1, 3, 10]
 
taulist = np.arange(-1,1, 0.01)*26


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
    averages.append(average_of_runs_files(label_folder, geometric))
    
    label_folder = results_path+DefaultInfo+descriptionOff+defaultangle +angle+ rho_ss_parameter + "/"
    labels.append(label_folder) 
    paths_array = get_array_of_runs_files(label_folder)
    averages.append(average_of_runs_files(label_folder, geometric))
     



except Exception as e:
#            print(e)
    print(traceback.format_exc())
    
   # print(sys.exc_info()[2])



at25_25 = averages[0]
#axs.set_title(DefaultInfo+description+defaultangle +angle)
axs.plot(at25_25[0]*26, at25_25[1], "r--" ,  linewidth=3 ,label = f"Simulation: Interaction on")   
axs.plot(-at25_25[0]*26, at25_25[1], "r--" , linewidth=3 )   




try:
    func = second_order_correlation_opposite_directions_interaction_on_empirical_araujo
    popt, pcov = curve_fit(func, at25_25[0], at25_25[1]) 
    plt.plot(at25_25[0]*26, func(at25_25[0], *popt), 'r-', linewidth=3, label=r'Empirical fit with interaction:' + "\n"+ ' $\Delta$=%5.2f, f=%5.2f, $\chi$=%5.2f' % tuple(popt))
except:
    print("ugly fit")
    pass



at25_25 = averages[1]
#axs.set_title(DefaultInfo+description[:-1]+defaultangle +angle)
#axs.set_title(r"$g^{(2)}(\tau)$ "+ "oppposite directions with" + f" $b_0 = {b0_input}, \Omega = {Omega}, \Delta $ = {Delta}$\Gamma$  ")
axs.plot(at25_25[0]*26, at25_25[1], "b--", linewidth=3 , label = f"Simulation: Interaction off")   
axs.plot(-at25_25[0]*26, at25_25[1],"b--", linewidth=3  )   

axs.set_xlabel(r"$\tau$ [ns]", fontsize=18)
axs.set_ylabel(r"$g^{(2)}(\tau)$")

#Curva Teo
g12 = second_order_correlation_opposite_directions_interaction_off_araujo(at25_25[0], float(Delta))
axs.plot(at25_25[0]*26, g12, label = r"Theory: single-scattering approach," + "\n" + "no interaction", c = "purple")
axs.plot(-at25_25[0]*26, g12, c= "purple")


#Curva fitada
axs.legend(loc='upper center', bbox_to_anchor=(0.5, -0.17),
          fancybox=True, shadow=True, ncol=2, prop={'size': 15})

general_name = results_path+DefaultInfo+description
    
plt.savefig(general_name + "nice_picture" + f"25_{angle}_manual_with_fit_comparison_mean_relatorio.png", dpi = 300, bbox_inches="tight")
    
#plt.ylim(0,10)
#plt.savefig(general_name + "s/N7_far_limavg.png")








