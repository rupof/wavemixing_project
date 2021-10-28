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

import sys




taulist = np.linspace(0,1, 100) 
Gamma = 1
Omega = 2
Delta = 20*Gamma
kd = 10


N = int(sys.argv[3]) 
psi0 = tensor([ket("1") for i in range(N) ])
wave_mixing = True
nhat = 0
ang1 = float(sys.argv[1]) 
ang2 = float(sys.argv[2])
R1 = get_nhat_from_angle(ang1)#1*xhat+ 10*yhat
R2 = get_nhat_from_angle(ang2)#1*xhat + 7*yhat #0.2*xhat+ 0.8*yhat

H, c_ops, GTensor,M, GammaSR, DeltaSR, Omega, SR_state, r = system_spec_N(Gamma, N, kd = kd, Delta = Delta, Omega = Omega, wave_mixing = wave_mixing)
g2_lig = g2_l(H, nhat, r, R1, R2, taulist, c_ops, N, faseglobal=False);

variables = r"$ \Gamma={0}, \Omega={1} \Gamma, \Delta = {2} , kd = {3}, N = {4} $".format(Gamma,Omega, Delta, kd, N)

end = timer()
np.savetxt("angulo{0}e{1}_N{3}_tempo{2}.txt".format(ang1,ang2,np.round(end-start,3),N), [taulist, np.real(g2_lig)])

#fig, ax = plt.subplots()  
#ax.plot(taulist, np.real(g2_lig)   )
#fig.savefig("testinho.png")
#plt.show()


print(end - start) # Time

