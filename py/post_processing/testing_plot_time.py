import numpy  as np
import matplotlib.pyplot as plt
from plots.multi_plots import *
import sys



fig, axs = plt.subplots(1, 3, figsize = (10,6) ,sharex = True, sharey = True)


angles = [str(25), str(90), str(155), "-"+str(25), "-"+str(90), str(205)]




N = str(sys.argv[1])
Omega = str(float(sys.argv[2]))
Delta = str(float(sys.argv[3]))
DefaultInfo = f"N{N}_Omega{Omega}_Delta{Delta}_"
description = str(sys.argv[4])
results_path = "../results/"
defaultangle = "25_"
get_time = True


g2_by_angle, g2_time = get_array_of_many_runs_usual_conditions(N, Omega, Delta, DefaultInfo, description, results_path, defaultangle, get_time)



at25_25 = g2_by_angle[0]
at25_90 =  g2_by_angle[1]
at25_155 = g2_by_angle[2]
at25_m25 = g2_by_angle[3]
at25_m90 = g2_by_angle[4]
at25_205 = g2_by_angle[5]




at_time25_25 = g2_time[0]
at_time25_90 =  g2_time[1]
at_time25_155 = g2_time[2]
at_time25_m25 = g2_time[3]
at_time25_m90 = g2_time[4]
at_time25_205 = g2_time[5]




print(at_time25_25)

avg = average_of_array_arrays(at_time25_155)

print("AVG", avg)














