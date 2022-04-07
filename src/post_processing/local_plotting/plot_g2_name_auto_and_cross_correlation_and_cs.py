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


fig, axs = plt.subplots(1, 2, figsize = (10,6) ,sharex = True, sharey = False)

axs_0_upper = axs[0].twiny()
axs_1_upper = axs[1].twiny()

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
geometric = True 
taulist = np.arange(-1,1, 0.01)


labels = []
averages = []
array_of_many_runs = []


angle_input =str(205)
angle = angle_input 
 
fig.suptitle(  f"N = {N}, b_0 = {b0_input}, Omega = {Omega}, Delta  = {Delta}, Geometric = {geometric}  ")

  #  try:
try: 
    label_folder = results_path+DefaultInfo+description+defaultangle +angle+ rho_ss_parameter + "/"
    labels.append(label_folder) 
    paths_array = get_array_of_runs_files(label_folder)
    #print(len(paths_array)
    
    runs_txt = get_array_of_numpy_runs(paths_array)
    avg = average_of_array_arrays(runs_txt[:], geometric)
    averages.append(avg)




except Exception as e:
#            print(e)
    print("Nao achouuuuuu")
    print(traceback.format_exc())
    
   # print(sys.exc_info()[2])



g2_12 = averages[0]
#axs[0].set_title(r"$g^{(2)}(\tau)$")
axs[0].plot(g2_12[0], g2_12[1], "b-" ,   linewidth=2 ,label = r"$g^{(2)}_{12}{(\tau)}$")   
#axs[0].plot(-g2_12[0], g2_12[1], "b-" ,  linewidth=0.5 )   

#axs[0].axhline(1)

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
    averages.append(average_of_runs_files(label_folder, geometric = geometric))

except Exception as e:
#            print(e)
    print(traceback.format_exc())

   # print(sys.exc_info()[2])


try:
    g2_11 = averages[0]
#axs[0].set_title("g^{(2)}_{11}")
    axs[0].plot(g2_12[0], g2_11[1], "r-" ,  linewidth=3 , label = r"$g^{(2)}_{11}{(\tau)}$")
#    axs[0].plot(-g2_12[0], g2_11[1], "r-",  linewidth=3  )
except:
    print(g2_11)



#ax0_y_ticks = np.append(axs[0].get_yticks(), [0.5])

# Set ytick locations to the values of the array `y_ticks`
#axs[0].set_yticks(ax0_y_ticks)

###################################################################################
# Cauchy-Schwarz
##############

print(len(g2_12[1]), len(g2_11[1]))
cs = cauchy_schwarz_from_g12_and_g22(g2_12[1], g2_11[1])

axs[1].plot(g2_12[0], cs, "r-", label = "C-S"  )

#axs[1].plot(-g2_12[0], cs, "r-"  )


axs[1].set_ylabel(r"$R$")
axs[1].set_xlabel(r"$\tau$ ")
axs[0].set_xlabel(r"$\tau$ ")
axs_0_upper.set_xlabel(r"$\tau$ [ns]")
axs_1_upper.set_xlabel(r"$\tau$ [ns]")

#print(axs[1].get_xticks())


axs_0_upper.plot(g2_12[0]*26, np.ones(len(g2_12[0]))) # Create a dummy plot
#axs_0_upper.cla()

axs_1_upper.plot(g2_12[0]*26, np.ones(len(g2_12[0]))) # Create a dummy plot
#axs_1_upper.cla()




axs[1].legend(loc='best', 
          fancybox=True, shadow=True, ncol=1, prop={'size': 15})


axs[0].set_ylabel(r"$g^{(2)}(\tau)$")
axs[0].legend(loc='best',
          fancybox=True, shadow=True, ncol=1, prop={'size': 15})

#axs[0].tick_params(axis='y', which='major', labelsize=8, rotation=0)
#axs[0].set_xlim(-15,15)
#axs[0].set_ylim(-0.5,3)
#axs[0].legend(loc='upper center', bbox_to_anchor=(0.5, -0.17),
#          fancybox=True, shadow=True, ncol=1, prop={'size': 15})

general_name = results_path+DefaultInfo+description

plt.tight_layout()
plt.savefig(general_name + "nice_picture_two_angles" + f"_cs_geometric_{geometric}.png", dpi = 300, bbox_inches="tight")
    
#plt.ylim(0,10)
#plt.savefig(general_name + "s/N7_far_limavg.png")








