import matplotlib.pyplot as plt
from plots.multi_plots import *



avg = average_of_runs_files("../results/N5_avg/")


fig = plt.figure(figsize = (5,7))
plt.plot(avg[0],avg[1])
plt.savefig("teste.png")
