#/usr/bin/env python
# coding: utf-8


from qutip import *
from helper_functions.operators import *
from timeit import default_timer as timer
from helper_functions.other import *
import sys


def manual_steadystate(H, c_ops, N, tmax, mc = False):
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
    if mc == True:
        print("psi0", dims(psi0))
        result = mcsolve(H, psi0, times, c_ops)
    else:
        result = mesolve(H, psi0, times, c_ops)
    return result.states[-1]

def get_steadystate(H, nhat, r,  taulist, c_ops, N, faseglobal = 1, rho_ss = None, rho_ss_parameter = "direct", tmax = None):
    """
    

    """

    start_time_ss = timer()
    if rho_ss_parameter == "manual":
        rho_ss = manual_steadystate(H, c_ops, N, tmax, mc = False)
    elif rho_ss_parameter == "manual_mc":
        print("dimH", dims(H))
        print("c_ops",c_ops)

        rho_ss = manual_steadystate(H, c_ops, N, tmax, mc = True)
    elif rho_ss_parameter[0:9] ==  "iterative":
        rho_ss = steadystate(H, c_ops, method = rho_ss_parameter, use_precond=True  )
    else:
        rho_ss = steadystate(H, c_ops, method = rho_ss_parameter, tol = 10**-20, maxiter = 10000*2)


    end_time_ss = timer()
    total_time_ss = end_time_ss - start_time_ss
    return rho_ss, total_time_ss





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
        - other methos available in QuTip
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

    if rho_ss is None:
        rho_ss, total_time_ss = get_steadystate(H, nhat, r, taulist, c_ops, N, faseglobal = 1, rho_ss = None, rho_ss_parameter = "direct", tmax = None)
    else:
        total_time_ss = 0

    ##Set error tolerance and more options
    options = Options( atol=1e-25)

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


    return np.real(g2_light), rho_ss, total_time_ss, total_time_correlation
#
##########################################

def g2_of_zero_subspace_approach( r, R1, R2, Beta1D, Beta2D, separated = None ):

    # implement if Beta1D and Beta2D is None, as with the exact case!!


    G2 = 0
    normalization = 0
    normalizationR1 = 0
    normalizationR2 = 0

    ####Change to correct implementation, considering just direct angle!
    k = 1

    moduleR1 = np.sqrt(R1.T @ (R1)).item()
    nhatR1 = R1/moduleR1

    moduleR2 = np.sqrt(R2.T @ (R2)).item()
    nhatR2 = R2/moduleR2
    ####
    N = len(r)
    for i in range(N):
        for ibar in range(N):
            

            phaseR1 = np.exp(-1j*k*( (nhatR1.T@(r[i]-r[ibar])).item())) 
            phaseR2 = np.exp(-1j*k*( (nhatR2.T@(r[i]-r[ibar])).item())) 
            
            #single excitation term
            normalizationR1 += phaseR1 * Beta1D[i]*np.conjugate(Beta1D[ibar])
            normalizationR2 += phaseR2 * Beta1D[i]*np.conjugate(Beta1D[ibar])
        
            
            for j in range(N):
                
                #double excitation term
                normalizationR1 += phaseR1*4*(Beta2D[i][j]*np.conjugate(Beta2D[ibar][j]))
                normalizationR2 += phaseR2*4*(Beta2D[i][j]*np.conjugate(Beta2D[ibar][j]))
                
                for jbar in range(N):
                    phase = np.exp(-1j*k*( (nhatR1.T@(r[j]-r[jbar])).item() + nhatR2.T@(r[i]-r[ibar])).item() )
                    G2 += phase*Beta2D[i][j]*np.conjugate(Beta2D[ibar][jbar]) #*4
                    
                    #sys.stdout.write("\r Summing on i =  {0} ".format(i))
                    #sys.stdout.flush()
                    #print(f"Summing on i = {i}, j = {ibar}, k = {j}, l = {jbar}")

    normalization = normalizationR1*normalizationR2
    

    if separated == True:
         return G2, normalization

    g2 = G2/normalization 
    

    return g2

def g2_dynamics_subspace_approach( r, R1, R2, taulist, Beta1D, Beta2D):
    """

    """

    g2_list = np.zeros_like(taulist)
    for t in range(len(taulist)):
        g2_list[t] = np.real(g2_of_zero_subspace_approach(r, R1, R2, Beta1D[t], Beta2D[t]))
    return g2_list, taulist

###########################

def cauchy_schwarz_from_g12_and_g22(g2_12, g2_11):
    """
    For a given g2 mixed and auto correlation   calculates Cauchy-Schwarz
    inequality as defined in Michelle O. Araújo, et all. P3: eq2:

    R = ( g1a2b(tau)* g1b2a(tau)) /( g1a1b(0) * g2a2b(0))

    where 1,2; 2,1 means opposite directions while 1,1 or 2,2 same direction.
    
    This program calculates R, using: 
    
    R = ( g_12(tau)* g_12(tau)) /( g_11(0) * g_11(0))
    
    Because g_11(0) = g_22(0) as proven in benchmarking notebook 
    """

    return g2_12*g2_12/(g2_11*g2_11)

def cauchy_schwarz(H, nhat, r, ang1, taulist, c_ops, N, faseglobal = 1, rho_ss = None, rho_ss_parameter = "direct", tmax = None):
    """
    For a given angle calculates Cauchy-Schwarz
    inequality as defined in Michelle O. Araújo, et all. P3: eq2:

    R = ( g1a2b(tau)* g1b2a(tau)) /( g1a1b(0) * g2a2b(0))

    where 1,2; 2,1 means opposite directions while 1,1 or 2,2 same direction.

    Algorithm:

    1-Define direction from input angle (ang1)
    2-Calculate g1a2b, g1b2a, g1a1b, g2a2b as functions of tau
    3-Grab  g1a1b, g2a2b of tau = 0
    4-Determine R and return R and rho_ss used


    Parameters
    ----------


    H : class:`qutip.Qobj`
        System Hamiltonian,
    n_hat : useless (REMOVE)
    r: useless (REMOVE)
    taulist: class: np.array
        list of times to run g2
    c_ops: list of :class:`qutip.Qobj`
        list of collapse operators
    N: int
        number of atoms
    faseglobal:  float
        simulation check to see if results are phase independent
    rho_ss: class:`qutip.Qobj`
        steady-state matrix. if not given and is calculated with rho_ss_parameter
    rho_ss_parameter: string
        method to calculate ss:
        - "direct" default method
        - "manual" evolving rho_ss
        - other method available in QuTip
    tmax: float
        time to evolve system in case "manual" is used

    Returns
    -------
    R: cauchy_schwarz fraction
    rho_ss: used steady-state


    """
    ang2 = 180+ang1
    R1 = get_nhat_from_angle(ang1)
    R2 = get_nhat_from_angle(ang2)
    


    
    g2_1a_2b, rho_ss, total_time_ss, total_time_correlation = g2_l(H, nhat, r, R1, R2, taulist, c_ops, N, faseglobal = 1, rho_ss = rho_ss, rho_ss_parameter = rho_ss_parameter, tmax = tmax)

    g2_l(H, nhat, r, R1, R2, taulist, c_ops, N, faseglobal = 1, rho_ss = rho_ss, rho_ss_parameter = rho_ss_parameter, tmax = tmax)

    extra_1a_2b = [rho_ss, total_time_ss, total_time_correlation]


    g2_1b_2a, *extra_1b_2a = g2_l(H, nhat, r, R2, R1, taulist, c_ops, N, faseglobal = 1, rho_ss =rho_ss , rho_ss_parameter = rho_ss_parameter, tmax=tmax)


    g2_1a_1b, *extra_1a_1a =  g2_l(H, nhat, r, R1, R1, taulist, c_ops, N, faseglobal = 1, rho_ss =rho_ss , rho_ss_parameter = rho_ss_parameter,tmax=tmax)



    g2_2a_2b, *extra_2b_2b = g2_l(H, nhat, r, R2, R2, taulist, c_ops, N, faseglobal = 1, rho_ss =rho_ss , rho_ss_parameter = rho_ss_parameter, tmax=tmax)

    g2_1a_1b_zero = g2_1a_1b[0]
    g2_2a_2b_zero = g2_2a_2b[0]

    R = (g2_1a_2b*g2_1b_2a)/(g2_1a_1b_zero*g2_2a_2b_zero)

    return np.real(R), rho_ss




def cauchy_schwarz_subspace(r, ang1,  Beta1D = None, Beta2D = None, taulist = np.linspace(0,1, 100), N_atoms = None , kd = None, b0 = None, exc_radius = None, Delta = None, Omega = None, wave_mixing = True, scalar = True, interaction = True, Sm_1D = None, Sm_2D = None  ):
    """
    For a given angle calculates Cauchy-Schwarz
    inequality as defined in Michelle O. Araújo, et al. P3: eq2:

    R = ( g1a2b(tau)* g1b2a(tau)) /( g1a1b(0) * g2a2b(0))

    where 1,2; 2,1 means opposite directions while 1,1 or 2,2 same direction.

    Algorithm:

    1-Define direction from input angle (ang1)
    2-Calculate g1a2b, g1b2a, g1a1b, g2a2b as functions of tau using subspace approach 
    3-Grab  g1a1b, g2a2b of tau = 0
    4-Determine R and return R and beta_i, beta_ij used 


    Parameters
    ----------


    H : class:`qutip.Qobj`
        System Hamiltonian,
    n_hat : useless (REMOVE)
    r: useless (REMOVE)
    taulist: class: np.array
        list of times to run g2
    c_ops: list of :class:`qutip.Qobj`
        list of collapse operators
    N: int
        number of atoms
    faseglobal:  float
        simulation check to see if results are phase independent
    rho_ss: class:`qutip.Qobj`
        steady-state matrix. if not given and is calculated with rho_ss_parameter
    rho_ss_parameter: string
        method to calculate ss:
        - "direct" default method
        - "manual" evolving rho_ss
        - other method available in QuTip
    tmax: float
        time to evolve system in case "manual" is used

    Returns
    -------
    R: cauchy_schwarz fraction
    rho_ss: used steady-state


    """

    if Beta1D and Beta2D is None:
        Beta1D, Beta2D, taulist, r = SolveForBeta1DandBeta2D_tau_QRT(N_atoms, kd, b0, exc_radius, Delta, Omega, wave_mixing, scalar, interaction, r, taulist, Sm_1D, Sm_2D)


    ang2 = 180+ang1
    R1 = get_nhat_from_angle(ang1)
    R2 = get_nhat_from_angle(ang2)

    g2_1a_2b = g2_dynamics_subspace_approach( r, R1, R2, taulist, Beta1D, Beta2D)
    g2_1b_2a = g2_dynamics_subspace_approach( r, R2, R1, taulist, Beta1D, Beta2D)
    g2_1a_1b = g2_dynamics_subspace_approach( r, R1, R1, taulist, Beta1D, Beta2D)
    g2_2a_2b = g2_dynamics_subspace_approach( r, R2, R2, taulist, Beta1D, Beta2D)

    g2_1a_1b_zero = g2_1a_1b[0]
    g2_2a_2b_zero = g2_2a_2b[0]

    R = (g2_1a_2b*g2_1b_2a)/(g2_1a_1b_zero*g2_2a_2b_zero)

    return np.real(R), [Beta1D, Beta2D]



















#### Benchmarking analytical functions

def second_order_correlation_opposite_directions_interaction_off_araujo(taulist, Delta):
    """
    For a given list of times(taulist) and detuning (Delta) calculates g2 of opposite directions
    (g2_12) for a typical four-wave-mixing experiment. More information in Michelle O. Araújo, et all. P1: eq1.

    Parameters
    ----------
    taulist: class: np.array
        list of times to run g2
    Delta: float
        detuning to be used

    Returns
    -------
    g12: second correlation function in opposite directions.

    """
    Gamma = 1
    g12 = 1+(4/np.pi**2)*(1+np.exp(-Gamma*np.abs(taulist))-2*np.cos(Delta*np.abs(taulist))*np.exp(-Gamma*np.abs(taulist)/2))
    return g12

def second_order_correlation_opposite_directions_interaction_on_empirical_araujo(taulist, DeltaExp, f, chi):
    """
    For a given list of times(taulist), detuning (Delta) and correction factor(chi )
    calculates g2 of opposite directions
    (g2_12) for empirical results of four-wave-mixing experiment reporte by Michelle O. Araújo, et all. This function is used to fit our simulations

    Parameters
    ----------
    taulist: class: np.array
        list of times to run g2
    DeltaExp: float
        detuning to be used

    chi: float
        correction factor in exponent

    Returns
    -------

    g12: second correlation function in opposite directions.

    """

    Gamma = 1

    g12 = 1+(f*4/np.pi**2)*(1+np.exp(-chi*Gamma*np.abs(taulist))-2*np.cos(DeltaExp*np.abs(taulist))*np.exp(-chi*Gamma*np.abs(taulist)/2))

    return g12
