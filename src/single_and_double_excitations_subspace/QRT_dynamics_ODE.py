import numpy as np
from scipy.integrate import solve_ivp, odeint
from copy import deepcopy, copy
from single_and_double_excitations_subspace.parameter_generator_for_ODE import *
from single_and_double_excitations_subspace.atomic_contributions_ODE import *
from helper_functions.cloud import *


    






def F_beta_double_exc_QRT(N, k, l, Beta1D, Beta2D, Delta1D, Omega1D, Sm_1D, Sm_2D, Delta2D):
    """
    This implementations considers that we are dealing with t large enough so that 〈σ−(t)〉 =〈σ−(t + τ) 〉


    """
    total_sum = 0
    total_sum += (1j*(Delta1D[k] + Delta1D[l])*Beta2D[k][l])
    total_sum += -1j * SumG_2D_first_term(N, Delta2D, Beta2D, k, l) #SumG_2D_first_term works for QRT but we have to use  Delta2D instead of G
    total_sum += -1j/2*(Omega1D[l]*Sm_1D[k] + Omega1D[k]*Sm_1D[l])  
    total_sum += -1j * SumG_2D_second_term(N, Delta2D, Sm_2D, k, l) #SumG_2D_second_term works for QRT but we have to use  Delta2D instead of G and Sm_2D instead Beta2D because we only have one time dependence in the operators
    return total_sum

def F_double_QRT(t,y, t_span, N_atoms, Beta1D, Omega1D,  Delta1D, Sm_1D, Sm_2D, Delta2D):
    """
    single and double excitation ODE
    #y = np.array([[Beta_0,Beta_1, ..., Beta_j, Beta_00, Beta_01, Beta_02, ... ,Beta_jm])
    """
    Beta2D = GetBeta_unflat(y, N_atoms, double = True) # getting coefficients: Beta2D = [[Beta11, Beta12, ...],[Beta21, Beta22, ...],...]
    
    F = GetBeta0_flat(N_atoms, double = True)
    try:
        #print(t)
        t_index = np.where(t==t_span)[0][0]
        #print("t", t, "t index", t_index) 
        for i in range(len(F)):
            k, l = index_to_row_major_order(i, N_atoms)
            F[i] = F_beta_double_exc_QRT(N, k, l, Beta1D, Beta2D, Delta1D, Omega1D, Sm_1D, Sm_2D, Delta2D) 
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
        
        F[i] = F_beta_double_exc_QRT(N_atoms, k, l, Beta1D, Beta2D, Delta1D, Omega1D, Sm_1D, Sm_2D, Delta2D)
        if k == l:
            F[i] = 0
            
    return F



def SolveForBeta1DandBeta2D_tau_QRT(N_atoms, kd = None, b0 = None, exc_radius = None, Delta = None, Omega = None, wave_mixing = True, scalar = True, interaction = True, r = None, taulist = np.linspace(0,1, 100)   ):
    
    t_span = taulist

    #t_span, dt = np.linspace(0,1,20, retstep = True) 
    
    BetaCoupled_flat = GetBeta0_flat(N_atoms, coupled = True)

    Delta1D, Omega1D, Gamma2D, Delta2D, r = GetAllODEParametersGiven_b0_or_kd(N_atoms, kd, b0, exc_radius, Omega, Delta, r, scalar)
    
    Sm_1D_time, Sm_2D_time, t_span_Sm, r = SolveForBeta1DandBeta2D(N_atoms, kd , b0 , exc_radius, Delta , Omega, wave_mixing, scalar, interaction, r, np.linspace(0,100, 30) )
    
    Sm_1D = Sm_1D_time[-1]
    Sm_2D = Sm_2D_time[-1]

    Solution = solve_ivp(F_coupled_QRT, (t_span[0], t_span[-1] ), BetaCoupled_flat, t_eval = t_span[:], args =( N_atoms, Omega1D,  Delta1D, Gamma2D,Sm_1D, Sm_2D , Delta2D))    
    BetaCoupled_solved = Solution.y.T
    t_span = Solution.t
    
    Beta1D_time_list = np.zeros(len(t_span), dtype = "object")
    Beta2D_time_list = np.zeros(len(t_span), dtype = "object")

    for l in range(len(t_span)):
        Beta1D_l, Beta2D_l = GetBeta_unflat(BetaCoupled_solved[l], N_atoms, coupled = True)
        Beta1D_time_list[l] = Beta1D_l
        Beta2D_time_list[l] = Beta2D_l
    
    return Beta1D_time_list, Beta2D_time_list, t_span, r 


