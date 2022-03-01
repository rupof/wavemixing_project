import numpy  as np
import matplotlib.pyplot as plt
from plots.multi_plots import *
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


fig, axs = plt.subplots(1, 2, figsize = (7,4) )

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
#t_list = [0.1, 0.5, 1, 3, 10]
 
geometric = True
taulist = np.arange(-1,1, 0.01)




angle_input =str(205)
angle = angle_input 
g2_max = []
N_list = [2,3,4,5,6,7]
for N in range(2,8):
  #  try:
    labels = []
    averages = []
    array_of_many_runs = []

    DefaultInfo = f"g2_N{N}_Omega{Omega}_Delta{Delta}_"

    try: 
        label_folder = results_path+DefaultInfo+description+defaultangle +angle+ rho_ss_parameter + "/"
        labels.append(label_folder) 
        paths_array = get_array_of_runs_files(label_folder)
        print(label_folder)
        number_of_runs = len(paths_array)
        averages.append(average_of_runs_files(label_folder, geometric))
        
        #label_folder = results_path+DefaultInfo+descriptionOff+defaultangle +angle+ rho_ss_parameter + "/"
        #labels.append(label_folder) 
        #paths_array = get_array_of_runs_files(label_folder)
        #averages.append(average_of_runs_files(label_folder))
         



    except Exception as e:
    #            print(e)
        print(traceback.format_exc())
        
       # print(sys.exc_info()[2])



    at25_25 = averages[0]
    #fig.suptitle(r"$g^{(2)}(\tau)$ "+ "oppposite directions with" + f" $b_0 = {b0_input}, \Omega = {Omega}, \Delta $ = {Delta}  ")
    axs[0].plot(at25_25[0]*26, at25_25[1],linewidth=3, label = f"N = {N}")  

    g2_max.append(max(at25_25[1]))
    
    axs[0].set_xlabel(r"$\tau$ [ns]", fontsize=18)
    axs[0].set_ylabel(r"$g^{(2)}(\tau)$", fontsize=18)

    axs[1].set_xlabel(r"N", fontsize=18)
    axs[1].set_ylabel(r"max($g^{(2)}(\tau)$)", fontsize=18)


    #axs[0].plot(-at25_25[0], at25_25[1], color=plt.gca().lines[-1].get_color() )   




    try:
        func = second_order_correlation_opposite_directions_interaction_on_empirical_araujo
        popt, pcov = curve_fit(func, at25_25[0], at25_25[1]) 
        plt.plot(taulist, func(taulist, *popt), color=axs[0].gca().lines[-1].get_color(), linestyle="--", label=f'Empirical fit N={N} ' + "\n"+ ' $\Delta$=%5.2f, f=%5.2f, $\chi$=%5.2f' % tuple(popt))
    except:
        print("ugly fit")
        pass




    axs[0].legend(loc = "best")

axs[1].scatter(N_list, g2_max, linewidth=3)


general_name = results_path+DefaultInfo+description

fig.tight_layout()

plt.savefig(general_name + "changing_n" + f"25_{angle}_manual_with_fit_comparison_mean_relatorio.png", dpi = 300)


#plt.ylim(0,10)
#plt.savefig(general_name + "s/N7_far_limavg.png")








