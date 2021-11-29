import numpy  as np
import matplotlib.pyplot as plt
from plots.multi_plots import *
import sys

fig, axs = plt.subplots(2, 3, figsize = (10,6) ,sharex = True, sharey = True)


angles = [str(25), str(90), str(155), "-"+str(25), "-"+str(90), str(205)]

N = str(sys.argv[1])
Omega = str(float(sys.argv[2]))
Delta = str(float(sys.argv[3]))
DefaultInfo = f"N{N}_Omega{Omega}_Delta{Delta}_"
description = str(sys.argv[4])
results_path = "../results/"
defaultangle = "25_"

labels = []
averages = []
array_of_many_runs = []



for i, angle in enumerate(angles):
  #  try:
        
        label = results_path+DefaultInfo+description+defaultangle +angle+"/"
        labels.append(label)
        paths_array = get_array_of_runs_files(label)

        averages.append(average_of_runs_files(label))
        
        array_of_many_runs.append(get_array_of_numpy_runs(paths_array))

        



# except:
   #     print(f"{angle} is missing")
 
#N7far25_25_avg =  average_of_runs_files("../results/N7_far/")

#N7far25_205_avg = average_of_runs_files("../results/N7_far25_205/")
#N7far25m25_avg = average_of_runs_files("../results/N7_far25m25/")
#N7far25_m90_avg = average_of_runs_files("../results/N7_far25_m90/")
#N7far25_155_avg = average_of_runs_files("../results/N7_far25_155/")
#N7far25_90_avg = average_of_runs_files("../results/N7_far25_90/")




at25_25 = averages[0]
at25_90 = averages[1]
at25_155 = averages[2]
at25_m25 = averages[3]
at25_m90 = averages[4]
at25_205 = averages[5]



axs[0, 0].plot(at25_25[0], at25_25[1], label = r"$ \theta_1 = {0} $ $  \theta_2 = {1} $".format(25,25))
axs[1, 0].plot(at25_m25[0], at25_m25[1], label = r"$ \theta_1 = {0}  $ $ \theta_2 = {1} $".format(25,-25))
axs[0, 1].plot(at25_90[0], at25_90[1], label = r"$ \theta_1 = {0} $ $ \theta_2 = {1} $".format(25,90))
axs[1, 1].plot(at25_m90[0], at25_m90[1], label = r"$ \theta_1 = {0}  $ $ \theta_2 = {1} $ ".format(25,-90))

axs[1, 2].plot(at25_205[0], at25_205[1], label = r"$ \theta_1 = {0}  $ $ \theta_2 = {1} $ ".format(25,205))
axs[0, 2].plot(at25_155[0], at25_155[1], label = r"$ \theta_1 = {0}  $ $ \theta_2 = {1} $ ".format(25,155))

#axs[0, 3].plot(at25_m90[0], at25_m90[1], label = r"$ \theta_1 = {0}  $ $ \theta_2 = {1} $ ".format(25,-90))




for i in range(len(axs)):
    for j in range(len(axs[i])):
        axs[i,j].legend()


general_name = results_path+DefaultInfo+description
    
plt.savefig(general_name + "avg.png")
    
#plt.ylim(0,10)
#plt.savefig(general_name + "s/N7_far_limavg.png")








