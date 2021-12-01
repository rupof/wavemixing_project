#!/usr/bin/env python
# coding: utf-8


from qutip import *
from helper_functions.operators import *
from timeit import default_timer as timer


def manual_steadystate(H, c_ops, N, tmax):
    times = np.arange(0,tmax,0.1)
    psi0 = tensor([ket("1") for i in range(N) ])
    result = mesolve(H, psi0, times, c_ops) 
    return result.states[-1]

def g2_l(H, nhat, r, R1, R2, taulist, c_ops, N, faseglobal = 1, rho_ss = None, rho_ss_parameter = "direct", tmax = None):
    k = 1
    
    if rho_ss == None:
        start_time_ss = timer()
        if rho_ss_parameter == "manual":
             rho_ss = manual_steadystate(H, c_ops, N, tmax)
        elif rho_ss_parameter[0:9] ==  "iterative": 
             rho_ss = steadystate(H, c_ops, method = rho_ss_parameter, use_precond=True  )
        else:
             rho_ss = steadystate(H, c_ops, method = rho_ss_parameter )

        
        end_time_ss = timer()
        total_time_ss = end_time_ss - start_time_ss


    ##Set error tolerance and more options
    options = Options( atol=1e-20)

    EmgR1  = Emg(N, r, R1, k, faseglobal)
    EmgR2  = Emg(N, r, R2, k, faseglobal)
    EpgR1  = Epg(N, r, R1, k, faseglobal)
    EpgR2  = Epg(N, r, R2, k, faseglobal)
    

    
    start_time_correlation = timer()

    G2 = correlation_3op_1t(H, rho_ss, taulist, c_ops, EmgR1, EmgR2 * EpgR2, EpgR1, options = options)
    
    Ep_R1_norm = EmgR1 * EpgR1
    Ep_R2_norm = EmgR2 * EpgR2
    
    normalization = (expect( Ep_R1_norm, rho_ss)) * (expect( Ep_R2_norm, rho_ss))
    
    g2_light = G2/normalization


    end_time_correlation = timer()

    total_time_correlation = end_time_correlation - start_time_correlation

    
    return g2_light, rho_ss, total_time_ss, total_time_correlation


# In[87]:


