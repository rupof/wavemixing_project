import sys
import julia
import numpy as np
import warnings
import time

#from helper_functions.cloud import *

from single_and_double_excitations_subspace.parameter_generator_for_ODE import *
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

def column(matrix, i, triD = False, j = 0):
    if triD != False:
        z_column = np.zeros(len(matrix))
        for z in range(len(matrix)):
            z_column[z] = matrix[z][i][j]
        return z_column  
    
    return [row[i] for row in matrix]

   

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


#r = random_cloud(r = None, N = N_atoms, exc_radius = None, b0 = b0)


### Python Subspace Approach


subspace_start = time.time()
Delta1D, Omega1D, Gamma2D, Delta2D, r = GetAllODEParametersGiven_b0_or_kd(N_atoms, kd, b0, exc_radius, Omega, Delta, r, scalar)
Beta1D_time_list, Beta2D_time_list, t_span, r = SolveForBeta1DandBeta2D(N_atoms, kd = None, b0 = None, exc_radius = None, Delta = Delta, Omega = Omega, wave_mixing = True, scalar = True, interaction = True, r = r, t_span = t_span  );


subspace_end = time.time()
subspace_time = subspace_end - subspace_start

### Python Exact Approach

qutip_start = time.time()

S_H, S_c_ops, GTensor,M, GammaSR, DeltaSR, Omega, SR_state, r = system_spec_N(1, N_atoms, kd = None, b0 = None, exc_radius = None , Delta = Delta, Omega = Omega, wave_mixing = True, scalar = True, r = r)
rho_ss_S, total_time_ss = get_steadystate(S_H, 0, r,  0, S_c_ops, N_atoms, faseglobal = 1, rho_ss = None, rho_ss_parameter = "direct", tmax = None)

S_sigmam_i_expectations = np.zeros(len(r), dtype = "object")
S_sigmam_ij_expectations = np.zeros((len(r),len(r)), dtype = "object")

for i in range(len(r)):
    S_sigmam_i_expectations[i] = expect(rho_ss_S, sigmam_i(N, i))
    for j in range(len(r)):
        S_sigmam_ij_expectations[i][j] = expect(rho_ss_S, sigmam_i(N, i)*sigmam_i(N, j))

qutip_end = time.time()
qutip_time = qutip_end-qutip_start



N=N_atoms
G=Gamma2D/2 + 1j*Delta2D 
Gamma1D = np.array([Gamma2D[j][j] for j in range(len(Gamma2D))])
Omega1D = Omega1D
Delta1D = Delta1D


#print("           ", G)
p = [N, G, Omega1D,Gamma1D ,  Delta1D]

print(p)

#Julia Subspace Approach
jl_ODE_start = time.time()
t, beta_jl_full = jl.benchmark_test(p)
jl_ODE_end = time.time()

jl_ODE_time = jl_ODE_end - jl_ODE_start

#print(len(beta_jl_full))
#print(len(beta_jl_full[0]))

#print(len(Beta1D_time_list))
plt.subplot(2, 1, 1)
plt.ylabel(r"$ \beta_{i} $")
plt.xlabel("t")



##plt.gca().set_title(r'$\beta_{i}()$')

beta_jl_full = np.array(beta_jl_full)

#print(len(beta_jl_full))
#print(len(beta_jl_full[0]))

for i in range(N): 

    plt.plot(t, beta_jl_full[i])
    plt.plot(t_span, column(Beta1D_time_list, i), "--")
    plt.plot(t_span, [np.real(S_sigmam_i_expectations[i]) for l in t_span],":" )    

plt.plot([0],[0], "r--", label = f"Python approximated " )
plt.plot([0],[0], "r:", label =  f"QuTip exact " )
plt.plot([0],[0], "r-", label = f"Julia approximated ")

plt.legend()


plt.subplot(2, 1, 2)
plt.ylabel(r"$ \beta_{ij} $")
plt.xlabel("t")


for j in range(N, len(beta_jl_full)):
    plt.plot(t,beta_jl_full[j])

for i in range(N):
    for j in range(N):
        plt.plot(t_span, column(np.real(Beta2D_time_list), i, True, j), "--")
        #plt.plot(t_span, [np.real(S_sigmam_ij_expectations[i][j]) for l in t_span],":"  )
        #print(i,j, " ",   np.real(S_sigmam_ij_expectations[i][j]) )

plt.savefig('benchmark_jl_py_nao_bate_double_rapido.png', bbox_inches='tight', dpi = 350)

print("Julia loading", jl_load_end - jl_load_start )
print("Julia ODE", jl_ODE_end-jl_ODE_start)

sys.exit(0)
