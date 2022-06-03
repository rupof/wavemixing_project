import sys
import julia
import numpy as np
import warnings
import time

#from helper_functions.cloud import *

from single_and_double_excitations_subspace.parameter_generator_for_ODE import *

from single_and_double_excitations_subspace.atomic_contributions_optimized_ODE import SolveForBeta1DandBeta2D_optimized
from single_and_double_excitations_subspace.atomic_contributions_ODE import *

from hamiltonian.hamiltonian_builder import *

from correlation.second_order_correlation  import *
from helper_functions.operators import *


import matplotlib.pyplot as plt 




warnings.filterwarnings("ignore", category=FutureWarning)

jl_load_start = time.time()
jl = julia.Julia(compiled_modules=False)
jl.include("./optimized_single_and_double_excitation/single_time_coefficients.jl")
jl_load_end = time.time()

 
N = N_atoms=int(sys.argv[1])
kd=None
exc_radius=None
b0=float(sys.argv[2] )
Omega=float(sys.argv[3])
Delta=float(sys.argv[4])
r = None
scalar = True

tf = 50.0
t_span = np.arange(0,tf,0.05 ) 

N_list = np.array([i for i in range(2, N, 3)])
time_list = np.zeros_like(N_list)
#r = random_cloud(r = None, N = N_atoms, exc_radius = None, b0 = b0)


### Python Subspace Approach

#for i in range(len(N_list)):
#    N_atoms =N_list[i]
#    N = N_list[i]
#    print("oi", N_atoms)
#    subspace_start = time.time()
    
#    Delta1D, Omega1D, Gamma2D, Delta2D, r = GetAllODEParametersGiven_b0_or_kd(N_atoms, kd, b0, exc_radius, Omega, Delta, r = None, scalar = True)
#    print(len(r))
#    Beta1D_time_list, Beta2D_time_list, t_span, r = SolveForBeta1DandBeta2D(N_atoms, kd = None, b0 = None, exc_radius = None, Delta = Delta, Omega = Omega, wave_mixing = True, scalar = True, interaction = True, r = r, t_span = t_span  );


#    subspace_end = time.time()
#    subspace_time = subspace_end - subspace_start
    
#    time_list[i] = subspace_time

#np.savetxt('subspace_time.csv', (N_list, time_list), delimiter=',')

#plt.plot(N_list, time_list, label = "Python")
#plt.yscale('log')


print("Subspace is saved!")

print("Beginning subspace opt")
### Python Subspace Optimized Approach

for i in range(len(N_list)):
    N_atoms = N_list[i]

    subspace_opt_start = time.time()
    
    Delta1D, Omega1D, Gamma2D, Delta2D, r = GetAllODEParametersGiven_b0_or_kd(N_atoms, kd, b0, exc_radius, Omega, Delta, r = None, scalar = True)
    Beta1D_opt_time_list, Beta2D_opt_time_list, t_span, r = SolveForBeta1DandBeta2D_optimized(N_atoms, kd = None, b0 = None, exc_radius = None, Delta = Delta, Omega = Omega, wave_mixing = True, scalar = True, interaction = True, r = r, t_span = t_span  );


    subspace_opt_end = time.time()
    subspace_opt_time = subspace_opt_end - subspace_opt_start

    time_list[i] = subspace_opt_time


np.savetxt('subspace_opt_time_2.csv', (N_list, time_list), delimiter=',')

plt.plot(N_list, time_list, label = "Python optimized")
### Python Exact Approach

#qutip_start = time.time()
#
#S_H, S_c_ops, GTensor,M, GammaSR, DeltaSR, Omega, SR_state, r = system_spec_N(1, N_atoms, kd = None, b0 = None, exc_radius = None , Delta = Delta, Omega = Omega, wave_mixing = True, scalar = True, r = r)
#rho_ss_S, total_time_ss = get_steadystate(S_H, 0, r,  0, S_c_ops, N_atoms, faseglobal = 1, rho_ss = None, rho_ss_parameter = "direct", tmax = None)
#
#S_sigmam_i_expectations = np.zeros(len(r), dtype = "object")
#S_sigmam_ij_expectations = np.zeros((len(r),len(r)), dtype = "object")
#
#for i in range(len(r)):
#    S_sigmam_i_expectations[i] = expect(rho_ss_S, sigmam_i(N, i))
#    for j in range(len(r)):
#        S_sigmam_ij_expectations[i][j] = expect(rho_ss_S, sigmam_i(N, i)*sigmam_i(N, j))
#
#qutip_end = time.time()
#qutip_time = qutip_end-qutip_start
#
#
#

print("beginnin Julia")
for i in range(len(N_list)):
    N_atoms = N_list[i]
    N=N_atoms
    

    Delta1D, Omega1D, Gamma2D, Delta2D, r = GetAllODEParametersGiven_b0_or_kd(N_atoms, kd, b0, exc_radius, Omega, Delta, r = None, scalar = True)

    G=Gamma2D/2 + 1j*Delta2D 
    Gamma1D = np.array([Gamma2D[j][j] for j in range(len(Gamma2D))])
    #print("           ", G)
    p = [int(N), G, Omega1D,Gamma1D ,  Delta1D]

    #print(p)

    #Julia Subspace Approach
    jl_ODE_start = time.time()
    t, beta_jl_full = jl.benchmark_test(p)
    jl_ODE_end = time.time()

    jl_ODE_time = jl_ODE_end - jl_ODE_start


    time_list[i] = jl_ODE_time


    np.savetxt('jl_ODE_time_2.csv', (N_list, time_list), delimiter=',')

plt.plot(N_list, time_list, label = "Pyjulia")

#print(len(beta_jl_full))
#print(len(beta_jl_full[0]))

#print(len(Beta1D_time_list))
plt.ylabel(r"time ")
plt.xlabel("N")




#plt.plot([0],[0], "r--", label = f"Python approximated " )
#plt.plot([0],[0], "r:", label =  f"QuTip exact " )
#plt.plot([0],[0], "r-", label = f"Julia approximated ")
#plt.plot([0],[0], "r-", label = f"Python Optimized ")


plt.legend()

plt.savefig(f"time_bench{N}.png", dpi = 300)
sys.exit(0)
