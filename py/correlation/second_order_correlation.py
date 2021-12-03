#!/usr/bin/env python
# coding: utf-8


from qutip import *
from helper_functions.operators import *
from timeit import default_timer as timer


def manual_steadystate(H, c_ops, N, tmax):
    """Evolution until tmax of a density matrix for a given Hamiltonian with N atoms and
    set of collapse operators.
    
    This function was thought-out for induced dipole-dipole interactions.


    Parameters
    ----------


    H : class:`qutip.Qobj`
        System Hamiltonian,
    c_ops : list of :class:`qutip.Qobj`
        list of collapse operators
    N: int
        number of atomsy
    tmax: float
        time to evolve system
    
    Returns
    -------

    result.states[-1]: rho0 at tmax 
    

    """

    times = np.arange(0,tmax,0.1)
    psi0 = tensor([ket("1") for i in range(N) ])
    result = mesolve(H, psi0, times, c_ops) 
    return result.states[-1]

def g2_l(H, nhat, r, R1, R2, taulist, c_ops, N, faseglobal = 1, rho_ss = None, rho_ss_parameter = "direct", tmax = None):
    """ 
    Second order correlation function as defined in R. Loudon P112 Eq (3.7.22): 
    g^{(2)} =  <E*(R1,t1)E*(R2, t2)E(R2, t2)E(R1, t1))>/  (<|E(R1, t1)|^2>><|E(R2, t2)|^2>)  
    => 
    g^{(2)} =  <E^-(R1, t)E^-(R2, t + tau)E^+(R2, t+tau)E^+(R1, t))>/
    (<E^-(R1, t)E^+(R1, t)>)(<E^-(R2, t))E^+(R2, t)>)

    For a given Hamiltonean using far field approximation.

    This function was thought-out for induced dipole-dipole interactions.

    Algorithm:

    1-Calculate steady-state (if not given ) and time it
    2-Create (far-field, pointing at R1 and R2) positive and negative electric fields operators
    using helper.functions.
    3-Calculate G2, using QuTip's correlation_3op_1t, 
    4-Calculate normalization, expecting out of steady state
    5-Get running time and return values


    Parameters
    ----------


    H : class:`qutip.Qobj`
        System Hamiltonian,
    n_hat : useless (REMOVE)
    r: useless (REMOVE)
    R1: class: np.array 
        1x3 array pointing to desired location (no need to be normalized)
    R2: class: np.array 
        1x3 array pointing to desired location (no need to be normalized)
    taulist: class: np.array
        list of times to run g2
    c_ops: list of :class:`qutip.Qobj`
        list of collapse operators
    N: int
        number of atoms
    faseglobal:  float
        simulation check to see if results are phase independent
    rho_ss: class:`qutip.Qobj`
        steady-state matrix. Normally it is not given and it is calculated
    rho_ss_parameter: string
        method to calculate ss: 
        - "direct" default method
        - "manual" evolving rho_ss 
        - other methos available at QuTip
    tmax: float
        time to evolve system in case "manual" is used

    Returns
    -------
    g2_light: second correlation function for given taulist, H and R1, R2
    
    rho_ss: used steady-state
    
    total_time_ss: time it took to calculate steady-state

    total_time_correlation: time it took to calculate expectation values of g2
    



    """





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


def second_order_correlation_opposite_directions_interaction_off_araujo(taulist, Delta):
    Gamma = 1

    g12 = 1+(4/np.pi**2)*(1+np.exp(-Gamma*np.abs(taulist))-2*np.cos(Delta*np.abs(taulist))*np.exp(-Gamma*np.abs(taulist)/2))

    return g12

def second_order_correlation_opposite_directions_interaction_on_empirical_araujo(taulist, DeltaExp, f, chi):
    Gamma = 1

    g12 = 1+(f*4/np.pi**2)*(1+np.exp(-chi*Gamma*np.abs(taulist))-2*np.cos(DeltaExp*np.abs(taulist))*np.exp(-chi*Gamma*np.abs(taulist)/2))

    return g12






