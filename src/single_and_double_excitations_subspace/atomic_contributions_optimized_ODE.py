import numpy as np
from scipy.integrate import solve_ivp, odeint
from copy import deepcopy, copy
from single_and_double_excitations_subspace.parameter_generator_for_ODE import *
from single_and_double_excitations_subspace.atomic_contributions_ODE import unflatten, flatten, row_major_order_to_index, index_to_row_major_order, G, GetBeta_tau0_flat, GetBeta0_flat, GetBeta_unflat

from helper_functions.cloud import *



def SumG_2D_optimized(G_val, beta):
    """
    \sum^N_{m!=l} G_lm \beta_km + \sum^N_{m!=k} G_km \beta_ml 

    summing on m

    We assume G_ll = 0
    """
    total_sum = np.einsum("lm, km", G_val, beta) +  np.einsum("km, ml", G_val, beta)
    return total_sum


  

def F_single_optimized(t,y, N_atoms, Omega1D,Delta1D,  Gamma2D, Delta2D):
    """
    Single and double excitation:
    #y = np.array([Beta_0,Beta_1, ..., Beta_j]) = Beta1D

    and the time derivatives: 
     
     F is the vector corresponding to the time derivative of the beta coefficients:
     F =[\dot{beta_1}, \dot{beta_2}, ..., \dot{beta_N}]
    """
    
    # getting coefficients from y:
    # Beta1D = [Beta_0, Beta_1, ..., Beta_N ]
    
    Beta1D = y  

  
    G_val = G(Gamma2D, Delta2D) 
    np.fill_diagonal(G_val,0)
    
    F = np.zeros((N_atoms), dtype = 'complex_') 
    
    #slow implementation: 
    #for l in range(0, N_atoms):
    #    F[l] = F_beta_single_exc_optimized(N_atoms, l, Beta1D, Delta1D, Omega1D, Gamma2D, Delta2D)
        
    #fast implementation:
    F[:N_atoms] = np.einsum("j,j->j", 1j*Delta1D-Gamma2D.diagonal()/2, Beta1D)- 1j*Omega1D/2    
    F[:N_atoms] -=  G_val @ Beta1D#.reshape(-1,1) 
       
    return F


def F_coupled_optimized(t,y, N_atoms, Omega1D,Delta1D,  Gamma2D, Delta2D, steady_state_interaction):
    """
    single and double excitation coupled ODE
    #y = np.array([Beta_0,Beta_1, ..., Beta_j, Beta_00, Beta_01, Beta_02, ... ,Beta_jm]) = Beta1D, Beta2D


    and the time derivatives: 
     
     F is the vector corresponding to the time derivative of the beta coefficients:
     F =[\dot{Beta_0}, \dot{Beta_1}, ..., \dot{Beta_N}, \dot{Beta_00}, \dot{Beta_01}, \dot{Beta_02}, ... ,\dot{Beta_jm} ]
    """
    
    # getting coefficients from y: 
    # Beta1D = [Beta_0, Beta_1, ..., Beta_N ]
    # Beta2D = [[Beta11, Beta12, ...,Beta1N],[Beta21, Beta22, ..., Beta2N],...,[BetaN1,..., BetaNN]]
    
    Beta1D, Beta2D =  GetBeta_unflat(y, N_atoms, coupled = True) 
  
    # Getting 1D F null vector
    # F will be the full 1D collapsed vector: 
    # F = np.array([[Beta_0,Beta_1, ..., Beta_j, Beta_00, Beta_01, Beta_02, ... ,Beta_jm])
    # len(F) = N_atoms + N_atoms*N_atoms 
     
    G_val = G(Gamma2D, Delta2D) 
    np.fill_diagonal(G_val,0)
    
    if steady_state_interaction == False: #i.e no interaction
        G_val *= 0

    F = GetBeta0_flat(N_atoms, coupled  = True)
    
    #SINGLE EXCITATION COEFFICIENTS

    #slow implementation:
    #for l in range(0, N_atoms):
    #    F[l] = F_beta_single_exc_optimized(N_atoms, l, Beta1D, Delta1D, Omega1D, Gamma2D, Delta2D)
    
    #fast implementation:
    F[:N_atoms] = np.einsum("j,j->j", 1j*Delta1D-Gamma2D.diagonal()/2, Beta1D)- 1j*Omega1D/2    
    F[:N_atoms] -=  G_val @ Beta1D   #.reshape(-1,1) 
    
    #DOUBLE EXCITATION COEFFICIENTS

    #slow implementation
    #for i in range(N_atoms,len(F)):
    #    k, l = index_to_row_major_order(i-N_atoms, N_atoms)   #troquei indice e funcionou
    #    k, l = np.unravel_index(i-N_atoms, (N_atoms, N_atoms)  )
   
    #    F[i] = F_beta_double_exc_optimized(N_atoms, k, l, Beta1D, Beta2D, Delta1D, Omega1D, Gamma2D, Delta2D)
    #    if k == l:
    #       F[i] = 0
        
 

    #fast implementation:

    F[N_atoms:] -= np.reshape( SumG_2D_optimized(G_val, Beta2D), len(F)-N_atoms) 
    F[N_atoms:] += np.reshape( np.einsum("l, kl->kl", 1j*Delta1D-Gamma2D.diagonal()/2, Beta2D)   + np.einsum("k, kl->kl", 1j*Delta1D-Gamma2D.diagonal()/2, Beta2D), len(F)-N_atoms)
    F[N_atoms:] -= np.reshape(1j/2*np.einsum("l,k->kl",Omega1D, Beta1D  ) +  1j/2*np.einsum("k,l->kl",Omega1D, Beta1D ), len(F)-N_atoms)
    

    F_temp = np.reshape(F[N_atoms:], [N_atoms, N_atoms])   #same as F[N_atoms:].reshape(N,N)
    np.fill_diagonal(F_temp,0) #i=j equal to zero
    F[N_atoms:] = F_temp.flatten() 
    
    return F
    


def SolveForBeta1D_optimized(N, kd = None, b0 = None, exc_radius = None, Delta = None, Omega = None, wave_mixing = True, scalar = True, interaction = True, r = None, t_span = None, initial_Beta1D = None ):
    
    
    Delta1D, Omega1D, Gamma2D, Delta2D, r = GetAllODEParametersGiven_b0_or_kd(N, kd, b0, exc_radius, Omega, Delta, r, scalar)
    if initial_Beta1D is not None:
        y0 = initial_Beta1D 
    else:
        y0 = GetBeta0_flat(N, double = False, coupled = False)
        
    Solution = solve_ivp(F_single_optimized, (t_span[0], t_span[-1] ), y0, t_eval = t_span[:], args = (N, Omega1D, Delta1D, Gamma2D, Delta2D))
    
    Beta1D_solved = Solution.y.T
    t_span = Solution.t
    
    Beta1D_time_list = np.zeros(len(t_span), dtype = "object")

    for l in range(len(t_span)):
        Beta1D_time_list[l] = Beta1D_solved[l]

   
    return Beta1D_time_list, t_span, r 


def SolveForBeta1DandBeta2D_optimized(N_atoms, kd = None, b0 = None, exc_radius = None, Delta = None, Omega = None, wave_mixing = True, scalar = True, interaction = True, r = None, t_span = None,  initial_Beta1D = None, initial_Beta2D = None, steady_state_interaction = True):
    

    #t_span, dt = np.linspace(0,1,20, retstep = True) 
    
    Delta1D, Omega1D, Gamma2D, Delta2D, r = GetAllODEParametersGiven_b0_or_kd(N_atoms, kd, b0, exc_radius, Omega, Delta, r, scalar)
    if initial_Beta1D is None and initial_Beta2D is None:
        BetaCoupled_flat = GetBeta0_flat(N_atoms, coupled = True)

    elif initial_Beta1D is not None and initial_Beta2D is None: 
        initial_Beta2D= np.zeros([N_atoms,N_atoms])
        BetaCoupled_flat = GetBeta_tau0_flat(initial_Beta1D , initial_Beta2D  )
        BetaCoupled_flat = np.array(BetaCoupled_flat,dtype="complex_")
    else: 
        BetaCoupled_flat = GetBeta_tau0_flat(initial_Beta1D , initial_Beta2D )
        BetaCoupled_flat = np.array(BetaCoupled_flat,dtype="complex_")


    Solution = solve_ivp(F_coupled_optimized, (t_span[0], t_span[-1] ), BetaCoupled_flat, t_eval = t_span[:], args =( N_atoms, Omega1D,  Delta1D, Gamma2D, Delta2D, steady_state_interaction ))    
    BetaCoupled_solved = Solution.y.T
    t_span = Solution.t
    
    Beta1D_time_list = np.zeros(len(t_span), dtype = "object")
    Beta2D_time_list = np.zeros(len(t_span), dtype = "object")

    for l in range(len(t_span)):
        Beta1D_l, Beta2D_l = GetBeta_unflat(BetaCoupled_solved[l], N_atoms, coupled = True)
        Beta1D_time_list[l] = Beta1D_l
        Beta2D_time_list[l] = Beta2D_l

    return Beta1D_time_list, Beta2D_time_list, t_span, r




#

