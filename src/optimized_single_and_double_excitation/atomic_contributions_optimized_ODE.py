import numpy as np
from scipy.integrate import solve_ivp, odeint
from copy import deepcopy, copy
from single_and_double_excitations_subspace.parameter_generator_for_ODE import *
from helper_functions.cloud import *


def unflatten(array1D, N):
    """
    transforms 1Darray to (N,N) dimensions
    """
    return array1D.reshape((N,N))

def flatten(array2D):
    """
    transform 2Darray to vector array 
    """
    return array2D.flatten()

def row_major_order_to_index(i, j, width):
    """
    i and j, start at 0:

             |-------- 5 ---------|
  Row      ______________________   _ _
   0      |0    1    2    3    4 |   |
   1      |5    6    7    8    9 |   3
   2      |10   11   12   13   14|  _|_
          |______________________|
Column     0    1    2    3    4

    """
    return i+width*j

def index_to_row_major_order(index, width):
    j = (int)(index / width)
    i = index - (j * width)
    return i, j

def G(Gamma2D, Delta2D):
    return Gamma2D/2 + 1j*Delta2D

def SumG_1D(N, G, beta, l):
    total_sum = 0
    for m in range(N):
        if m != l:
            total_sum += G[l][m]*beta[m] 
    return total_sum

def SumG_2D_optimized(G, beta):
    """
    \sum^N_{m!=l} G_lm \beta_km

    summing on m
    """
    total_sum = np.einsum("lm, km->kl", G, beta, optimize = True) +  np.einsum("km, ml->kl", G, beta, optimize = True)

    return total_sum


def F_beta_single_exc(N, l, Beta1D, Delta1D, Omega1D, Gamma2D, Delta2D):
    G_val = np.fill_diagonal(G(Gamma2D, Delta2D),0)
    #print("Delta", Delta2D[l][l])
    #print("Delta1D", Delta1D[l]) 
    #print("Gamma", Gamma2D[l])
    #print("Beta", Beta1D)
    #print("Omega", Omega1D)

    return (1j*Delta1D[l]-Gamma2D[l][l]/2)*Beta1D[l]-1j*Omega1D[l]/2

def F_beta_double_exc(N, k, l, Beta1D, Beta2D, Delta1D, Omega1D, Gamma2D, Delta2D):
    Gval = np.fill_diagonal(G(Gamma2D, Delta2D), 0)
     
    total_sum = 0
    total_sum += (1j*(Delta1D[k] + Delta1D[l])-0.5*(Gamma2D[k][k]+Gamma2D[l][l]))*Beta2D[k][l] 
    total_sum += -1j/2*(Omega1D[l]*Beta1D[k]+Omega1D[k]*Beta1D[l])
    total_sum += -SumG_2D_optimized(Gval, Beta2D)[k][l]

    return total_sum

def GetBeta_tau0_flat(Beta1D, Beta2D ):
    Beta_double = flatten(Beta2D)
    Beta_flat = np.hstack((Beta1D, Beta_double))
    return Beta_flat

def GetBeta0_flat(N_atoms, double = False, coupled = False):
    if coupled == True:
       Beta_single = np.zeros((N_atoms), dtype = 'complex_')       #beta_i [beta_1, beta_2, ..., beta_N_atoms]
       Beta_double = flatten(np.zeros((N_atoms, N_atoms), dtype = 'complex_')) #beta_ij [beta_11, beta_12, ... beta_N_atomsN_atoms]
       Beta_flat = np.hstack((Beta_single, Beta_double) ) # np.array([[Beta_0,Beta_1, ..., Beta_j, Beta_00, Beta_01, Beta_02, ... ,Beta_jm])
    elif double == True:
       Beta_double = flatten(np.zeros((N_atoms, N_atoms), dtype = 'complex_')) #beta_ij [beta_11, beta_12, ... beta_N_atomsN_atoms]
       Beta_flat = Beta_double
    else:
        Beta_single = np.zeros((N_atoms), dtype = 'complex_')  
        Beta_flat = Beta_single
    return Beta_flat
    


def GetBeta_unflat(Beta_flat, N_atom, double = False, coupled = False):
    if coupled == True:
        Beta_single = deepcopy(Beta_flat[:N_atom])
        Beta_double = unflatten(Beta_flat[N_atom:], N_atom )
        return Beta_single, Beta_double
    elif double == True:
        Beta_double = unflatten(Beta_flat, N_atom)
        return Beta_double
    else:
        Beta_single = deepcopy(Beta_flat[:N_atom])
    


def F_single(t,y, N_atoms, Omega1D,Delta1D,  Gamma2D, Delta2D):
    """
    single and double excitation ODE
    #y = np.array([Beta_0,Beta_1, ..., Beta_j]) = Beta1D

    """
    #print("important", y)
    
    

    Beta1D = y  
    F = np.zeros(N_atoms, dtype = 'complex_') 


    for l in range(0, N_atoms):
        F[l] = F_beta_single_exc(N_atoms, l, Beta1D, Delta1D, Omega1D, Gamma2D, Delta2D)    
    return F

def F_double(t,y, t_span, N_atoms, Beta1D, Omega1D,  Delta1D, Gamma2D, Delta2D):
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
            F[i] = F_beta_double_exc(N_atoms, k, l, Beta1D[t_index], Beta2D, Delta1D, Omega1D, Gamma2D, Delta2D)
    except:
        print("opa")
        
    return F

def F_coupled(t,y, N_atoms, Omega1D,Delta1D,  Gamma2D, Delta2D):
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
    
    F[:N_atoms] -=  G_val @ Beta1D.reshape(-1,1) 
    
    for i in range(N_atoms,len(F)):
        #k, l = index_to_row_major_order(i-N_atoms, N_atoms)   #troquei indice e funcionou
        k, l = np.unravel_index(i-N_atoms, (N_atoms, N_atoms)  )
        
   
        F[i] = F_beta_double_exc(N_atoms, k, l, Beta1D, Beta2D, Delta1D, Omega1D, Gamma2D, Delta2D)
        if k == l:
            F[i] = 0
        
    return F








def SolveForBeta1D(N, kd = None, b0 = None, exc_radius = None, Delta = None, Omega = None, wave_mixing = True, scalar = True, interaction = True, r = None, t_span = np.linspace(0,1, 100) ):
    
    Delta1D, Omega1D, Gamma2D, Delta2D, r = GetAllODEParametersGiven_b0_or_kd(N, kd, b0, exc_radius, Omega, Delta, r, scalar)
    Beta1D = solve_ivp(F_single, t_span, y0, args = (N_atoms, Delta1D, Omega1D, Gamma2D, Delta2D))
    
    return Beta1D, r 


def SolveForBeta1DandBeta2D(N_atoms, kd = None, b0 = None, exc_radius = None, Delta = None, Omega = None, wave_mixing = True, scalar = True, interaction = True, r = None, t_span = None  ):
    

    #t_span, dt = np.linspace(0,1,20, retstep = True) 
    
    BetaCoupled_flat = GetBeta0_flat(N_atoms, coupled = True)

    Delta1D, Omega1D, Gamma2D, Delta2D, r = GetAllODEParametersGiven_b0_or_kd(N_atoms, kd, b0, exc_radius, Omega, Delta, r, scalar)

     
    Solution = solve_ivp(F_coupled, (t_span[0], t_span[-1] ), BetaCoupled_flat, t_eval = t_span[:], args =( N_atoms, Omega1D,  Delta1D, Gamma2D, Delta2D))    
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

