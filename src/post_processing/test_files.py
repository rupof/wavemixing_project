import numpy  as np
import matplotlib.pyplot as plt
from file_manager.visualization_preparation_tools import *
import sys
import traceback
import re

sys.stdout = open('log.txt', 'w')

angles = [str(25), str(90), str(155), "-"+str(25), "-"+str(90), str(205)]

f_bashes= open("bashes.txt", "a") 
f_bash_g2= open("bash_g2.txt", "a") 




c1 = [2.0,20.0]
c2 = [0.02, 0.0]
c3 = [1.0, 0.0]

c_list = [c1,c2,c3]
N_list = [i for i in range(1,8)]
b0_list = [0.1, 3, 5]
interaction_list = [True, False]
interaction_string = ["On", "Off"]
useb0 = 1
kd = None
rho_ss_parameter = "direct"

results_path = "../results/"
defaultangle = "25_"
default_sbatch = "sbatch send_multiple_jobs_rho_ss_subarray.sh"



ang1 = 25
tmax=0
num_runs = 100
print("c_list:", c_list)




listOfg2Problems = [[],[],[],[],[],[],[]]
listOfrhoProblems = [[],[],[],[],[],[],[]]
listOfNotFounds = [0 for i in range(8)]

def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

for N in N_list:
    counter = 0
    not_found_counter = 0
    not_found_rhoss_counter = 0
    for b0 in b0_list:
        for l in range(len(interaction_list)):
            interaction = interaction_list[l]
            interaction_str = interaction_string[l]
            description = f"b0_{b0}_V_Int_{interaction_str}_fixed_"
            for c_i in c_list:
                Omega, Delta = float(c_i[0]), float(c_i[1])
                DefaultInfo = f"g2_N{N}_Omega{Omega}_Delta{Delta}_"

                counter += 1 

                label = results_path+DefaultInfo[3:]+description + rho_ss_parameter + "/"
                if os.path.isdir(label) == False:
                    listOfrhoProblems[N-1].append(label)
                    # [f"interaction = {l} \n c_i = {c_i} \n b0 = {b0}", label])                      
                    not_found_rhoss_counter += 1
                    
                    f_bashes.write(default_sbatch + f" {N} {useb0} {b0} {description} {num_runs} {int(interaction)} {Omega} {Delta} {rho_ss_parameter} 0 \n")

                else: 
                    for i, angle in enumerate(angles):
                        try:
                            label = results_path+DefaultInfo+description+defaultangle +angle +"_" + rho_ss_parameter + "/"
                            paths_array = get_array_of_runs_files(label)
                        except:
                            txt = f"get_g2_from_all_available_rho_ss({ang1},{angle}, {N}, {useb0}, {b0}, 0 , \"{description}\", {interaction}, {Omega}, {Delta}, \"{rho_ss_parameter}\", {tmax} ) \n"

                            f_bash_g2.write(txt)



                        #listOfg2Problems[N-1].append(f"interaction = {interaction_list[l]} \n c_i = {c_i} \n b0 = {b0}")
                #not_found_counter +=1
    listOfNotFounds[N-1] = [0, not_found_rhoss_counter]







print("Report, not found:")
for N in range(len(listOfg2Problems)):
    print("----------------------- \n")
    print("N=", N+1, ": \n ", )
    print("rhoss problems") 
    for Problem in natural_sort(listOfrhoProblems[N]):
        print(Problem)
    print(f"\n not found {listOfNotFounds[N][1]}/{counter}" ) 
    print("----------------------")
    print("g2 problems") 
    #for Problem in natural_sort(listOfg2Problems[N]):
    #    print(Problem)
    print(f"\n not found {listOfNotFounds[N][0]}/{counter}" )
    print("------------------------ \n")




sys.stdout.close()
















