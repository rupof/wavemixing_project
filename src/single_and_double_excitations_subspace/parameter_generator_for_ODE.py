import numpy as np
from scipy.integrate import solve_ivp
from copy import deepcopy
from hamiltonean_builder import * 
from helper_functions.cloud import *




def GetOmega1D(Omega, r):
    k = 1
    kvec = k*yhat # incident laser propagating direction


    Omega1D = np.zeros(len(r), dtype = 'complex_') 
    for i in range(len(r)):
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


def GetAllODEParametersGiven_r(Omega, Delta, r, scalar = True):
    Omega1D = GetOmega1D(Omega, r) 
    Delta1D = GetDelta1D(Delta, r) 
    Delta2D, Gamma2D = GetDelta2DAndGamma2D(r, scalar =  True) 

    return  Delta1D, Omega1D, Gamma2D, Delta2D


def GetAllODEParametersGiven_b0_or_kd(N = None, kd = None, b0 = None, exc_radius = None, Omega = None, Delta = None, r = None, scalar = True):
    if r is None:
        if kd != None: #if cloud radius is given!
            radius =  kd/k
            r = random_cloud(radius, N, exc_radius, b0 )
        elif b0 != None: #if b0 is given!
            r = random_cloud(None,N,exc_radius, b0)
            print("r", r)

    
    Delta1D, Omega1D, Gamma2D, Delta2D = GetAllODEParametersGiven_r(Omega, Delta, r, scalar = True)
    
    return  Delta1D*0.5, Omega1D*0.5, Gamma2D*0.5, Delta2D  , r

