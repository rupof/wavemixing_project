import numpy  as np
import matplotlib.pyplot as plt
from plots.multi_plots import *

fig, axs = plt.subplots(2, 3, figsize = (10,6) ,sharex = True, sharey = True)


N7far25_25_avg =  average_of_runs_files("../results/N7_far/")

N7far25_205_avg = average_of_runs_files("../results/N7_far25_205/")
N7far25m25_avg = average_of_runs_files("../results/N7_far25m25/")
N7far25_m90_avg = average_of_runs_files("../results/N7_far25_m90/")

N7far25_155_avg = average_of_runs_files("../results/N7_far25_155/")

N7far25_90_avg = average_of_runs_files("../results/N7_far25_90/")










at25_25 = N7far25_25_avg
at25_m25 = N7far25m25_avg
at25_m90 = N7far25_m90_avg 
at25_90 = N7far25_90_avg 
at25_155 = N7far25_155_avg
at25_205 = N7far25_205_avg


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


plt.savefig("../results/plot_results/N7_far_avg.png")
plt.ylim(0,10)
plt.savefig("../results/plot_results/N7_far_limavg.png")








