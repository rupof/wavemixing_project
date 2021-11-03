#!/usr/bin/env python
# coding: utf-8

import numpy as np
from qutip import *

from helper_functions.interaction_preparation import *
from helper_functions.operators import *
from helper_functions.other import *
from helper_functions.cloud import *




def GreensTensor_and_SRstate(Gamma, N, r, scalar = False):
    """ For a given Gamma, N and r 
    returns: Green's tensor, M matrix, Δ matrix,  Γ matrix, ΓSR, ΔSR and SR state
    
    """
    k = 1

    GTensor = np.zeros([N,N], dtype = "object")
    GammaMatrix = np.zeros([N,N])
    DeltaMatrix = np.zeros([N,N])  
    
    
    for i, r_i in enumerate(r):
        for j, r_j in enumerate(r):
            Gij = Gij_calc(Gamma, k, r, i, j, scalar)     
            
            Deltaij = Deltaij_calc(Gij, scalar)
            Gammaij = Gammaij_calc(Gij, scalar)
            
            GTensor[i][j] = Gij
            
            DeltaMatrix[i][j] = Deltaij 
            GammaMatrix[i][j] = Gammaij
            
            
    M = GammaMatrix   + 1j*DeltaMatrix
    eigenvalues, eigenvectors, GammaSR, DeltaSR, SR_state = Get_SR(M)
    
    return GTensor, M, DeltaMatrix, GammaMatrix, GammaSR, DeltaSR, SR_state


def system_spec_N(Gamma, N , kd = None, b0 = None, exc_radius = None, Delta = None, Omega = None, wave_mixing = True, scalar = False ):
    k = 1
    kvec = k*yhat # incident laser propagating direction
    
    print("b0 system", b0)
    print("kd system", kd)
    if kd != None: #if cloud radius is given!
        radius =  kd/k
        r = random_cloud(radius, N, exc_radius, b0 )
    elif b0 != None: #if b0 is given!
        print(b0)
        r = random_cloud(None,N,exc_radius, b0)  
    
    GTensor, M, DeltaMatrix, GammaMatrix, GammaSR, DeltaSR, SR_state = GreensTensor_and_SRstate(Gamma, N , r, scalar)

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



