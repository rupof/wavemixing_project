import numpy as np
from scipy.integrate import solve_ivp, odeint
from copy import deepcopy, copy
from single_and_double_excitations_subspace.parameter_generator_for_ODE import *
from single_and_double_excitations_subspace.atomic_contributions_ODE import *
from helper_functions.cloud import *


    

def SumG_2D_QRT(N, G, beta, k, l):
    """
    \sum^N_{m!=k} G_mk \beta_lm

    summing on m
    """
    total_sum = 0
    for m in range(N):
        if m != l:
            total_sum += G[l][m]*beta[k][m] 
    return total_sum





def F_beta_double_exc_QRT(N, k, l, Beta1D, Beta2D, Delta1D, Omega1D, Sm_1D, Sm_2D, Gamma2D, Delta2D):
    """
    This implementations considers that we are dealing with t large enough so that 〈σ−(t)〉 =〈σ−(t + τ) 〉


    """
    G_val = G(Gamma2D, Delta2D)

    total_sum = 0
    total_sum += (1j*(Delta1D[l])  - 0.5*(Gamma2D[l][l]))*Beta2D[k][l] #  *0.5
    total_sum += -1j/2*(Omega1D[l]*Sm_1D[k])  #*0.5
    total_sum += - SumG_2D_QRT(N, G_val, Beta2D, k, l)
    return total_sum

def F_double_QRT(t,y, t_span, N_atoms, Beta1D, Omega1D,  Delta1D, Sm_1D, Sm_2D, Gamma2D, Delta2D):
    """
    single and double excitation ODE
    #y = np.array([[Beta_0,Beta_1, ..., Beta_j, Beta_00, Beta_01, Beta_02, ... ,Beta_jm])
    """
    Beta2D = GetBeta_unflat(y, N_atoms, double = True) # getting coefficients: Beta2D = [[Beta11, Beta12, ...],[Beta21, Beta22, ...],...]
    
    F = GetBeta0_flat(N_atoms, double = True)
    try:
        #print(t)
        #t_index = np.where(t==t_span)[0][0]
        #print("t", t, "t index", t_index) 
        for i in range(len(F)):
            k, l = index_to_row_major_order(i, N_atoms)
            F[i] = F_beta_double_exc_QRT(N, k, l, Beta1D, Beta2D, Delta1D, Omega1D, Sm_1D, Sm_2D, Gamma2D, Delta2D) 
    except:
        print("opa")
    return F


def F_coupled_QRT(t,y, N_atoms, Omega1D,Delta1D,Gamma2D, Sm_1D, Sm_2D, Delta2D):
    """
    single and double excitation ODE
    #y = np.array([Beta_0,Beta_1, ..., Beta_j, Beta_00, Beta_01, Beta_02, ... ,Beta_jm])
    """
    # getting coefficients from y: 
    # Beta1D = [Beta_0, Beta_1, ..., Beta_N ]
    # Beta2D = [[Beta11, Beta12, ...,Beta1N],[Beta21, Beta22, ..., Beta2N],...,[BetaN1,..., BetaNN]]
    
    Beta1D, Beta2D =  GetBeta_unflat(y, N_atoms, coupled = True) 
  
    # Getting 1D F null vector
    # F will be the full 1D collapsed vector: 
    # F = np.array([[Beta_0,Beta_1, ..., Beta_j, Beta_00, Beta_01, Beta_02, ... ,Beta_jm])
    # len(F) = N_atoms + N_atoms*N_atoms 
    
    F = GetBeta0_flat(N_atoms, coupled  = True)
    
    for l in range(0, N_atoms):
        F[l] = F_beta_single_exc(N_atoms, l, Beta1D, Delta1D, Omega1D, Gamma2D, Delta2D)

    for i in range(N_atoms,len(F)):
        #k, l = index_to_row_major_order(i-N_atoms, N_atoms)   #troquei indice e funcionou
        k, l = np.unravel_index(i-N_atoms, (N_atoms, N_atoms)  )
        
        F[i] = F_beta_double_exc_QRT(N_atoms, k, l, Beta1D, Beta2D, Delta1D, Omega1D, Sm_1D, Sm_2D, Gamma2D, Delta2D)
        #if k == l:
        #    F[i] = 0
            
    return F



def SolveForBeta1DandBeta2D_tau_QRT(N_atoms, kd = None, b0 = None, exc_radius = None, Delta = None, Omega = None, wave_mixing = True, scalar = True, interaction = True, r = None, taulist = np.linspace(0,1, 100), Sm_1D = None, Sm_2D = None  ):
    
    Delta1D, Omega1D, Gamma2D, Delta2D, r = GetAllODEParametersGiven_b0_or_kd(N_atoms, kd, b0, exc_radius, Omega, Delta, r, scalar)
    
    
    # Obtain approximated approach  Sm_1D = 〈σ−(t)〉 =〈σ−(t + τ) 〉 and  Sm_2D = 〈σ−(t+ τ)σ−(t+ τ)〉 =〈σ−(t+ τ)σ−(t + τ) 〉

    Sm_1D_time, Sm_2D_time, t_span_Sm, r = SolveForBeta1DandBeta2D(N_atoms, kd , b0 , exc_radius, Delta , Omega, wave_mixing, scalar, interaction, r, np.linspace(0,400, 50) )
    
    # If Sm_1D is given by exact approach ignore, if not use approximated approach value  
    if Sm_1D is None and Sm_2D is None:    
        Sm_1D = Sm_1D_time[-1]
        Sm_2D = Sm_2D_time[-1]

    
    BetaCoupled_flat = GetBeta_tau0_flat(Sm_1D, Sm_2D)
    BetaCoupled_flat = np.array(BetaCoupled_flat,dtype="complex_")


    Solution = solve_ivp(F_coupled_QRT, (taulist[0], taulist[-1] ), BetaCoupled_flat, t_eval = taulist[:], args =( N_atoms, Omega1D,  Delta1D, Gamma2D,Sm_1D, Sm_2D , Delta2D))    
    BetaCoupled_solved = Solution.y.T
    taulist = Solution.t
     
    Beta1D_time_list = np.zeros(len(taulist), dtype = "object")
    Beta2D_time_list = np.zeros(len(taulist), dtype = "object")

    for l in range(len(taulist)):
        Beta1D_l, Beta2D_l = GetBeta_unflat(BetaCoupled_solved[l], N_atoms, coupled = True)
        Beta1D_time_list[l] = Beta1D_l
        Beta2D_time_list[l] = Beta2D_l
    
    return Beta1D_time_list, Beta2D_time_list, taulist, r 


