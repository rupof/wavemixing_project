#!/usr/bin/env python
# coding: utf-8

import numpy as np
from qutip import *

from helper_functions.interaction_preparation import *
from helper_functions.operators import *
from helper_functions.other import *
from helper_functions.cloud import *




def GreensTensor_and_SRstate(Gamma, N, kd = 0.10):
    """ For a given Gamma, N and kd, 
    returns: Green's tensor, M matrix, Δ matrix,  Γ matrix, ΓSR, ΔSR and SR state
    
    """
    k = 1
    d =  kd/k 
    r = np.array([generate_atom_r(i*d) for i in range(N)])

    GTensor = np.zeros([N,N], dtype = "object")
    GammaMatrix = np.zeros([N,N])
    DeltaMatrix = np.zeros([N,N])  
    
    
    for i, r_i in enumerate(r):
        for j, r_j in enumerate(r):
            Gij = Gij_calc(Gamma, k, r, i, j)     
            
            Deltaij = Deltaij_calc(Gij)
            Gammaij = Gammaij_calc(Gij)
            
            GTensor[i][j] = Gij
            
            DeltaMatrix[i][j] = Deltaij 
            GammaMatrix[i][j] = Gammaij
            
            
    M = GammaMatrix   + 1j*DeltaMatrix
    eigenvalues, eigenvectors, GammaSR, DeltaSR, SR_state = Get_SR(M)
    
    return GTensor, M, DeltaMatrix, GammaMatrix, GammaSR, DeltaSR, SR_state


def system_spec_N(Gamma, N , kd = 10, Delta = None, Omega = None, wave_mixing = True ):
    k = 1
    kvec = k*yhat # incident laser propagating direction
    
    radius =  kd/k
    
    r = random_cloud(radius, N)
    
    GTensor, M, DeltaMatrix, GammaMatrix, GammaSR, DeltaSR, SR_state = GreensTensor_and_SRstate(Gamma, N , kd)

    if Delta == None: #For Delta = DeltaSR  
        Delta = DeltaSR
        Omega = 0.1*0.5*DeltaSR
    else: #Given Delta
        Delta;
        #print(DeltaSR)
        if Omega == None: #For a given Delta and no Omega
            Omega = 0.1*0.5*DeltaSR
            #print(Omega)
        elif Omega != None:  #For a given Delta and Omega
            Omega;
    
        
    c_ops = []
    H = 0
    Hint = 0
    Lij = 0
    
    if wave_mixing == True:
        for i, r_i in enumerate(r):
            H += -Delta * sigmap_i(N,i) * sigmam_i(N,i)
    
            #Wave 1
            H += 1/2*( Omega* ( (np.exp( 1j*(kvec.T@r[i]).item())*sigmap_i(N,i) + np.exp(-1j*(kvec.T@r[i]).item())*sigmam_i(N,i) ))) 
            #Wave 2
            H += 1/2*( Omega* ( (np.exp(-1j*(kvec.T@r[i]).item())*sigmap_i(N,i) + np.exp( 1j*(kvec.T@r[i]).item())*sigmam_i(N,i) ))) 

            
            for j, r_j in enumerate(r):
                Deltaij = DeltaMatrix[i][j]
                Gammaij = GammaMatrix[i][j]


                Hint +=  Deltaij * sigmap_i(N,i) * sigmam_i(N,j)
                Lij = 0.5*Gammaij*( (2*spre(sigmam_i(N,i))*spost(sigmap_i(N,j))) -1.0*spre(sigmap_i(N,j)*sigmam_i(N,i)) - 1.0*spost(sigmap_i(N,j)*sigmam_i(N,i)))

                c_ops.append(Lij)
    else:    
        for i, r_i in enumerate(r):

            H += identity_wrap(N, i, -Delta*(sigmap()*sigmam()) )
            H += identity_wrap(N, i, 1/2*(Omega* sigmap() + Omega* sigmam() ))  

            for j, r_j in enumerate(r):
                Deltaij = DeltaMatrix[i][j]
                Gammaij = GammaMatrix[i][j]


                Hint +=  Deltaij * sigmap_i(N,i) * sigmam_i(N,j)
                Lij = 0.5*Gammaij*( (2*spre(sigmam_i(N,i))*spost(sigmap_i(N,j))) -1.0*spre(sigmap_i(N,j)*sigmam_i(N,i)) - 1.0*spost(sigmap_i(N,j)*sigmam_i(N,i)))

                c_ops.append(Lij)
 

    Htot = H + Hint            


    return Htot, c_ops, GTensor, M, GammaSR, DeltaSR, Omega, SR_state, r



