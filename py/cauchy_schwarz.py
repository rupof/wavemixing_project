import matplotlib.pyplot as plt
import numpy as np
from qutip import *
from timeit import default_timer as timer

start = timer()


from helper_functions.interaction_preparation import *
from helper_functions.operators import *
from helper_functions.other import * 
from hamiltonean_builder.hamiltonean_builder import *
from correlation.second_order_correlation import *
from file_manager import get_path_to_save_files, get_new_run_number_txt, save_params_to_file, save_rhoss_to_file, get_new_run_number_dat



import sys




taulist = np.linspace(0,1, 100) 
Gamma = 1
nhat = 0

ang1 = float(sys.argv[1])
print(f"ang1 = {ang1}")
ang2 = float(sys.argv[2]) ##This is a useless parameter
print(f"ang2 = {ang2}")
N = int(sys.argv[3]) 
print(f"N = {N}")
useb0 = bool(int(sys.argv[4]))
print(f"useb0 = {useb0}")
if useb0 == True:
    b0 = float(sys.argv[5])
    kd = None
    exc_radius = None
    description = str(sys.argv[6])
    print(f"b0 = {b0}, description = {description}")
    # ang1 ang2 N useb0 b0 description interaction Omega Delta
else:
    b0 = None
    kd = float(sys.argv[5])
    exc_radius = float(sys.argv[6])
    description = str(sys.argv[7])
    # ang1 ang2 N useb0 kd exc_radius description    
    print("kd main", kd) 
interaction = bool(int(sys.argv[7]))
print(f"interaction = {interaction}")
Omega = float(sys.argv[8])*Gamma
print(f"Omega = {Omega}")
Delta = float(sys.argv[9])*Gamma
print(f"Delta = {Delta}")
rho_ss_parameter = str(sys.argv[10])
print(f"rho_ss_parameter = {rho_ss_parameter}")
tmax = float(sys.argv[11])
print(f"tmax = {tmax}")




psi0 = tensor([ket("1") for i in range(N) ])
wave_mixing = True
scalar = False




description += f'_{int(ang1)}_{rho_ss_parameter}'

if tmax != 0:
    description += f'_{tmax}'


H, c_ops, GTensor,M, GammaSR, DeltaSR, Omega, SR_state, r = system_spec_N(Gamma, N, kd = kd, b0 = b0, exc_radius = exc_radius , Delta = Delta, Omega = Omega, wave_mixing = wave_mixing, scalar = scalar)

R, rho_ss= cauchy_schwarz(H, nhat, r, ang1, taulist, c_ops, N, faseglobal = False, rho_ss = None, rho_ss_parameter = rho_ss_parameter, tmax = tmax)



variables = r"$ \Gamma={0}, \Omega={1} \Gamma, \Delta = {2} , kd = {3}, N = {4}, b0 = {5} $".format(Gamma,Omega, Delta, kd, N, b0)

variables_string = "Gamma={0} \nOmega={1}*Gamma \nDelta = {2} \nkd = {3} \nN = {4}  \nb0 = {5}\nscalar = {6}, interaction = {7} ".format(Gamma,Omega, Delta, kd, N, b0, scalar , interaction)



end = timer()

#Saving files!

        
path_to_save_file = get_path_to_save_files(N, Omega, Delta,  description)
filename ="{4}/angulo{0}_N{3}_Omega{5}_Delta{6}_run".format(ang1,ang2,0,N,path_to_save_file, Omega, Delta) 
run_number = get_new_run_number_dat(filename)
name_of_file =  "{4}/angulo{0}_N{3}_Omega{5}_Delta{6}_run{2}".format(ang1,ang2,run_number,N, path_to_save_file, Omega, Delta)
name_of_file_time =  "{4}/time/time_angulo{0}_N{3}_Omega{5}_Delta{6}_run{2}.txt".format(ang1,ang2,run_number,N, path_to_save_file, Omega, Delta)

save_params_to_file(variables_string, filename)


#np.savetxt(name_of_file, [taulist, R])
#np.savetxt(name_of_file_time, [total_time_ss, total_time_correlation] ) 

save_rhoss_to_file(rho_ss, name_of_file)
#fig, ax = plt.subplots()  
#ax.plot(taulist, np.real(g2_lig)   )
#fig.savefig("testinho.png")
#plt.show()


print(end - start) # Time

