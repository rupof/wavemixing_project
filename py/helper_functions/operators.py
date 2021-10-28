import numpy as np
from qutip import *
from helper_functions.constants import *


def identity_wrap(N, index, element):
    """
    Wraps an element in tensor identity products

    N: 2^N size of hillbert space
    index: position in tensor product, ie:  I x I x I x A[index] x I
    element: desired element to wrap in 
    
    """
    identities = [qeye(2) for i in range(N)] # = I_1, I_2, I_3, ...
    identities[index] = element
    return tensor(identities)

def sigmam_i(N,j):


    return identity_wrap(N,j, sigmam())


    
def sigmap_i(N,j):
    return identity_wrap(N,j, sigmap())

def excited_population_at_time_t(N, result, t):
    n = 0
    for i in range (N):
            n_i_operator = sigmap_i(N,i) * sigmam_i(N,i)
            n += expect(n_i_operator, result.states[t]) 
    return n

def Ep(N, r, nhat, k = 1):
    Ep = 0
    for i in range (N):
            Ep +=  np.exp(-1j*k* (nhat.T@r[i]).item()) * sigmam_i(N,i)
    return Ep
def Em(N, r, nhat, k = 1):
    Em = 0
    for i in range (N):
            Em +=  np.exp( 1j*k* (nhat.T@r[i]).item() ) * sigmap_i(N,i) 
    return Em

def Epg(N, r, R, k = 1, faseglobal = 1):
    """Positive Electric Field operator for:
    N: number of atoms, 
    r: array of position vectors of atoms
    R: vector of desired position
    """
    Ep = 0
    moduleR = np.sqrt(R.T @ (R)).item()
    nhat = R/moduleR
    if faseglobal != 1:
        faseglobal =  np.exp(-1j*k*moduleR)/moduleR
    
    for i in range (N):
            Ep +=  faseglobal * np.exp(-1j*k* (nhat.T@r[i]).item()) * sigmam_i(N,i)
    return Ep

def Emg(N, r, R, k = 1, faseglobal = 1):
    """Negative Electric Field operator for:
    N: number of atoms, 
    r: array of position vectors of atoms
    R: vector of desired position
    """
    Em = 0
    moduleR = np.sqrt(R.T @ (R)).item()
    nhat = R/moduleR
    if faseglobal != 1:
        faseglobal =  np.exp(1j*k*moduleR)/moduleR
    for i in range (N):
            Em +=  faseglobal * np.exp( 1j*k* (nhat.T@r[i]).item() ) * sigmap_i(N,i) 
    return Em


