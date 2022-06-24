import sys
import numpy as np
import warnings
import time

#from helper_functions.cloud import *

from single_and_double_excitations_subspace.parameter_generator_for_ODE import *

from single_and_double_excitations_subspace.atomic_contributions_optimized_ODE import SolveForBeta1DandBeta2D_optimized

from hamiltonian.hamiltonian_builder import *

from correlation.second_order_correlation  import *
from helper_functions.operators import *


import matplotlib.pyplot as plt 




warnings.filterwarnings("ignore", category=FutureWarning)

 
N = N_atoms=300 #int(sys.argv[1])
kd=None
exc_radius=None
b0=0.1 # float(sys.argv[2] )
Omega= 2# float(sys.argv[3])
Delta=20 #float(sys.argv[4])
r = None
scalar = True

tf = 50.0
t_span = np.arange(0,tf,0.05 ) 

N_list = np.logspace(2, 8, num=16, base=2, dtype = "int")
time_list = np.zeros_like(N_list)
#r = random_cloud(r = None, N = N_atoms, exc_radius = None, b0 = b0)


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


np.savetxt('subspace_opt_time_new_3.csv', (N_list, time_list), delimiter=',')


