#!/usr/bin/env python
# coding: utf-8


from qutip import *
from helper_functions.operators import *


def g2_l(H, nhat, r, R1, R2, taulist, c_ops, N, faseglobal = 1):
    k = 1
    
    rho_ss = steadystate(H, c_ops)
    
    EmgR1  = Emg(N, r, R1, k, faseglobal)
    EmgR2  = Emg(N, r, R2, k, faseglobal)
    EpgR1  = Epg(N, r, R1, k, faseglobal)
    EpgR2  = Epg(N, r, R2, k, faseglobal)
    
    G2 = correlation_3op_1t(H, rho_ss, taulist, c_ops, EmgR1, EmgR2 * EpgR2, EpgR1)
    
    Ep_R1_norm = EmgR1 * EpgR1
    Ep_R2_norm = EmgR2 * EpgR2
    
    normalization = (expect( Ep_R1_norm, rho_ss)) * (expect( Ep_R2_norm, rho_ss))
    
   
    
    g2_light = G2/normalization

    return g2_light


# In[87]:


