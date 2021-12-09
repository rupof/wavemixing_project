import numpy as np
from helper_functions.constants import *


def Gij_calc(Gamma, k, positions, i, j, scalar = False):
    """
    Get Gij matrix of Green's tensors G for a dipole-dipole interaction as
    given in A. Cidrim, et all (2020) (Eq. 3). 

    If scalar is True, it returns an scalar model interaction Gij

    Parameters:
    ----------

    Gamma: float
        decaying rate, normally equal to 1
    k: float
        wavenumber, normally equal to 1
    positions:
        array of atoms positions, some methods for different positions generation
        are implemented, i.e linear chain and random cloud.

    i, j: integers
        index of atoms 
    scalar: boolean
        if True uses scalar model
    """

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
    """
    Calculates inelastic term Γij matrix of dipolar interaction as given in
    A. Cidrim, et all (2020):

    Γij =  ϵˆi 2Img(G ij)ϵˆj , where ϵˆi is the polarization of the
ith dipole, which we choose to be ϵˆi = ϵ̂ = ẑ.

    """
    if scalar == False:
        Gammaij = ( zhat.T @ (2 * np.imag(Gij) ) @ zhat ).item()
    elif scalar == True:
        
        if Gij == 0:
            Gammaij = 2
        else:
            Gammaij = 2*np.sin(Gij)/Gij
    return Gammaij

def Deltaij_calc(Gij, scalar = False):
    """
    Calculates elastic term Δij matrix of dipolar interaction as given in
    A. Cidrim, et all (2020):

    Δij =  ϵˆi real(-G ij)ϵˆj , where ϵˆi is the polarization of the
ith dipole, which we choose to be ϵˆi = ϵ̂ = ẑ.
    
    NOTE:
    -------
    There is an error in A. Cidrim, et all (2020) paper definition, we need to
    add a minus inside Δij, as done above. 

    """
    if scalar == False:
        Deltaij = ( zhat.T @( -1*np.real(Gij) )  @ zhat ).item()
    elif scalar == True:  
        if Gij == 0:
            Deltaij = 0
        else:
            Deltaij = -1*np.cos(Gij)/Gij
    return Deltaij





