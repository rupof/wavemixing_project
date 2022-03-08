#!/usr/bin/env python
# coding: utf-8

import numpy as np
from qutip import *

from helper_functions.interaction_preparation import *
from helper_functions.operators import *
from helper_functions.other import *
from helper_functions.cloud import *




def GreensTensor_and_SRstate(Gamma, N, r, scalar = False):
    """ 
    Obtains full Green's tensor matrix containing 3x3 matrices for each matrix element 
    for a given set of positions r for N atoms and Gamma decaying rate. Furthermore,
    it obtains superradiant state: M matrix, Δ matrix,  Γ matrix, ΓSR, ΔSR and SR state.

    Returns: 

    Green's tensor, M matrix, Δ matrix,  Γ matrix, ΓSR, ΔSR and SR state
    
    """
    k = 1

    GTensor = np.zeros([N,N], dtype = "object") # dtype = "object" is necessary to insert 3x3 matrices in array.

    GammaMatrix = np.zeros([N,N])
    DeltaMatrix = np.zeros([N,N])      
    
    for i, r_i in enumerate(r):
        for j, r_j in enumerate(r):
            Gij = Gij_calc(Gamma, k, r, i, j, scalar) #Calculates Gij 3x3 matrix     
            GTensor[i][j] = Gij #Inserts Gij matrix in Gtensor

            Deltaij = Deltaij_calc(Gij, scalar)
            Gammaij = Gammaij_calc(Gij, scalar)
            
            DeltaMatrix[i][j] = Deltaij 
            GammaMatrix[i][j] = Gammaij
            
            
    M = GammaMatrix   + 1j*DeltaMatrix
   
    eigenvalues, eigenvectors, GammaSR, DeltaSR, SR_state = Get_SR(M)
    
    return GTensor, M, DeltaMatrix, GammaMatrix, GammaSR, DeltaSR, SR_state


def system_spec_N(Gamma, N , kd = None, b0 = None, exc_radius = None, Delta = None, Omega = None, wave_mixing = True, scalar = False, interaction = True, r = None ):
    """
    This function creates the hamiltonean and collapsible operators of our system
    "ground-state neutral atoms that interact solely through induced dipole-
    dipole interactions and have a simple two-level internal structure."
    as described by A. Cidrim, et all (2020) (Eq. 2 and 3). 


    Parameters
    ----------
    Gamma: integer
        decaying rate
    N: integer
        number of atoms
    kd: float
        cloud radius
    b0: float
        optical depth, if given a predefined formula is used 
        to calculate exc_radius. See cloud.py
    exc_radius: float
        if b0 is not given (kd is given) user has
        to give size of exclusion radius
    Omega: float
        laser Rabi frequency
    wave_mixing: boolean
        True by defaults. It means that we are going to use 
        four-wave-mixing configuration. That is, two counter propagating waves.
    scalar: boolean
        If true we use scalar model and not vector model for interactions
    interaction: boolean
        If False we turn off interactions in hamiltonean and lindbladian collapsible operators.
        Default is True (interactions on)


    Algorithm
    --------
    

   


    """

    k = 1
    kvec = k*yhat # incident laser propagating direction
    
    print("b0 system", b0)
    print("kd system", kd)
    
    try:
            if r == None:
                if kd != None: #if cloud radius is given!
                    radius =  kd/k
                    r = random_cloud(radius, N, exc_radius, b0 )
                elif b0 != None: #if b0 is given!
                    print(b0)
                    r = random_cloud(None,N,exc_radius, b0)  
    except:
        print( "r is an array")
        
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

                Hint_ij =  Deltaij * sigmap_i(N,i) * sigmam_i(N,j)
                Lij = 0.5*Gammaij*( (2*spre(sigmam_i(N,i))*spost(sigmap_i(N,j))) -1.0*spre(sigmap_i(N,j)*sigmam_i(N,i)) - 1.0*spost(sigmap_i(N,j)*sigmam_i(N,i)))
 

                if interaction == False: #Without interaction mixed terms are nulled       
                    if i != j:
                        Lij  *= 0
                        Hint_ij *= 0
                
                Hint += Hint_ij 
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



