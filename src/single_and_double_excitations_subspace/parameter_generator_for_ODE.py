import numpy as np
from scipy.integrate import solve_ivp
from copy import deepcopy
from hamiltonian.hamiltonian_builder import *
from hamiltonian.different_waves import *
from helper_functions.cloud import *




def GetOmega1D(Omega, r, beam = "plane_wave", b0 = 0.1):
    """Omega1D is the same thing as OmegaN"""
    k = 1
    kvec = k*yhat # incident laser propagating direction
    Omega1D = np.zeros(len(r), dtype = 'complex_') 
    
    for i in range(len(r)):
        if beam == "Gaussian":
            try:
                R =  get_radius_from_optical_thickness(len(r),b0)
                w0 = R/2
                Omega1D[i] = (Omega*Gaussian_beam(r[i], w0)).item()
            except:
                print("Problem with gaussian beam")
        else:
            Omega1D[i] = Omega*(np.exp(1j*(kvec.T@r[i]).item()) + np.exp(-1j*(kvec.T@r[i]).item()))
    return Omega1D
         
def GetDelta1D(Delta, r):
    k = 1
    Delta1D = np.zeros(len(r)) 
    for i in range(len(r)):
        Delta1D[i] = Delta
    return Delta1D
  
      
def GetDelta2DAndGamma2D(r, scalar =  True):
    Gamma = 1
    N = len(r)
    GTensor, M, Delta2D, Gamma2D, GammaSR, DeltaSR, SR_state = GreensTensor_and_SRstate(Gamma, N, r, scalar)
    
    return Delta2D, Gamma2D


def GetAllODEParametersGiven_r(Omega, Delta, r, beam = "plane_wave", b0 = 0.1, scalar = True):
    Omega1D = GetOmega1D(Omega, r, beam = beam, b0 = b0) 
    Delta1D = GetDelta1D(Delta, r) 
    Delta2D, Gamma2D = GetDelta2DAndGamma2D(r, scalar =  True) 

    return  Delta1D, Omega1D, Gamma2D, Delta2D


def GetAllODEParametersGiven_b0_or_kd(N = None, kd = None, b0 = None, exc_radius = None, Omega = None, Delta = None, r = None, scalar = True, beam = "plane_wave"):
    if r is None:
        if kd != None: #if cloud radius is given!
            radius =  kd/k
            r = random_cloud(radius, N, exc_radius, b0 )
        elif b0 != None: #if b0 is given!
            r = random_cloud(None,N,exc_radius, b0)
            print("r", r)

    
    Delta1D, Omega1D, Gamma2D, Delta2D = GetAllODEParametersGiven_r(Omega, Delta, r, b0, beam, scalar)
    
    return  Delta1D, Omega1D, Gamma2D, Delta2D  , r

