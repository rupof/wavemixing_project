import numpy  as np
import matplotlib.pyplot as plt
from plots.multi_plots import *
import sys
import traceback
from correlation import *
from scipy.optimize import curve_fit
from matplotlib.pyplot import cm


import warnings
warnings.filterwarnings("error")

fig, axs = plt.subplots(1, 1, figsize = (10,6) ,sharex = True, sharey = True)

######

### Interaction On
#b0_input = str(sys.argv[1])
N = str(sys.argv[1])
Omega = str(float(sys.argv[2]))
Delta = str(float(sys.argv[3])) 
DefaultInfo = f"N{N}_Omega{Omega}_Delta{Delta}_"
description = str(sys.argv[4]) #f"b0_{b0_input}_V_Int_On_"
#descriptionOff = f"b0_{b0_input}_V_Int_Off_"
rho_ss_parameter = str(sys.argv[5])
results_path = "../results/"
defaultangle = "25_"


#t_list = [0.1, 0.5, 1, 3, 10]
t_list_T = [1]
taulist = np.arange(-1,1, 0.01)


labels = []
averages = []
array_of_many_runs = []


angle_input =str(25)
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

  #  try:
try: 
    label_folder =  results_path+"cauchy_schwarz_" + DefaultInfo+description+defaultangle + rho_ss_parameter + "/"
    labels.append(label_folder) 
    paths_array = get_array_of_runs_files(label_folder)
    averages.append(average_of_runs_files(label_folder))
    array_of_many_runs.append(get_array_of_numpy_runs(paths_array))
    



except Exception as e:
    #print(t, angle)
#            print(e)
    print(traceback.format_exc())
    
   # print(sys.exc_info()[2])



at25_25 = averages[0]
axs.set_title(DefaultInfo+description+defaultangle )
axs.plot(at25_25[0], at25_25[1], "r--", -at25_25[0], at25_25[1], "r--" , label = f"Simulation, Int: On-avg")   

at25 = get_list_organized_by_pairs(array_of_many_runs[0])
print(len(at25))
color = iter(cm.rainbow(np.linspace(0, 1, len(at25))))
for i in range(0,int(len(at25)), 2):
    c = next(color)
    print(c)
    axs.plot(at25[i], at25[i+1], c = c, label = f"run {i/2}")
    axs.plot(-at25[i], at25[i+1], c = c )

axs.legend()



#try:
#    func = second_order_correlation_opposite_directions_interaction_on_empirical_araujo
#    popt, pcov = curve_fit(func, at25_25[0], at25_25[1]) 
#    plt.plot(taulist, func(taulist, *popt), 'r-', label='fit: Delta=%5.3f, f=%5.3f, chi=%5.3f' % tuple(popt))
#except:
#    print("ugly fit")
#    pass




#Curva Teo
#g12 = second_order_correlation_opposite_directions_interaction_off_araujo(taulist, float(Delta))
#axs.plot(taulist, g12, label = "Theory")

#Curva fitada

#axs.legend()


general_name = results_path+DefaultInfo+description
    
plt.savefig(general_name + f"{angle}_cs_all.png")
    
plt.ylim(0,10)
plt.savefig(general_name + f"{angle}_lim_cs_all.png")








