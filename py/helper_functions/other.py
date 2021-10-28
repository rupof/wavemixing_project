import numpy as np
from qutip import *
from  helper_functions.constants import * 




def get_vector_components(R):
    x,y,z = R[0] , R[1], R[2]
    return x,y,z
def get_nhat_from_angle(degrees):
    theta = 2*3.14/360*degrees
    a = np.cos(theta)
    b = np.sin(theta)
    nhat = (a*xhat+b*yhat)/(a**2+b**2)**0.5
    return nhat

def generate_atom_r(x):
    r_atom = np.array([[x],[0],[0]])
    return r_atom

def linear_chain(d, N):
    r = np.array([generate_atom_r(i*d) for i in range(N)])
    return r

def Get_SR(M):
    eigenvalues, eigenvectors = np.linalg.eig(M)
    largest_real_eigval_index = np.where( np.real(eigenvalues) == max(np.real(eigenvalues)))[0][0]
    Gamma_SR, Delta_SR = np.real(eigenvalues[largest_real_eigval_index]), np.imag(eigenvalues[largest_real_eigval_index])
    SR_state = Qobj(eigenvectors[largest_real_eigval_index])

    return eigenvalues, eigenvectors, Gamma_SR, Delta_SR, SR_state






