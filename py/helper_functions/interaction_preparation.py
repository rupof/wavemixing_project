import numpy as np
from helper_functions.constants import *



def Gij_calc(Gamma, k, positions, i, j, scalar = False):
    r_i = positions[i]
    r_j = positions[j]
    r_ij = r_i-r_j
    r_ij_norm = np.linalg.norm(r_ij)
        
    if scalar == False:
        
        if np.array_equal(r_i,r_j) == True:
            Gij = Gamma*0.5j*I3 
        else:   
            Gij = (3*Gamma/4)* (np.exp(1j*k*r_ij_norm)/(k*r_ij_norm)**3) * ( (k**2*r_ij_norm**2 + 1j*k*r_ij_norm - 1 )*I3 - (k**2*r_ij_norm**2 + 3j*k*r_ij_norm - 3) * ((r_ij @ r_ij.T)/r_ij_norm**2) )

    elif scalar == True: 
        Gij = np.linalg.norm(r_ij)*k #norm(k) 
    return Gij

def Gammaij_calc(Gij, scalar = False):
    if scalar == False:
        Gammaij = ( zhat.T @ (2 * np.imag(Gij) ) @ zhat ).item()
    elif scalar == True:
        
        if Gij == 0:
            Gammaij = 2
        else:
            Gammaij = 2*np.sin(Gij)/Gij
    return Gammaij

def Deltaij_calc(Gij, scalar = False):
    if scalar == False:
        Deltaij = ( zhat.T @( -1*np.real(Gij) )  @ zhat ).item()
    elif scalar == True:
         
        if Gij == 0:
            Deltaij = 0
        else:
            Deltaij = -1*np.cos(Gij)/Gij
        print(Deltaij)
    return Deltaij





