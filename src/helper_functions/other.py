import numpy as np
from qutip import *
from  helper_functions.constants import * 


def relative_error(A,B):
    try:
        return np.average(np.abs((A-B)/(A+B)), axis = 0)
    except:
        return (np.abs((A-B)/(A+B)))

def get_vector_components(R):
    x,y,z = R[0] , R[1], R[2]
    return x,y,z
def get_nhat_from_angle(degrees, phi = 90 ):
    """
    get normal 2d vector pointing in "degrees" direction
    """
    theta = 2*3.1415/360.0*degrees
    phi = 2*3.1415/360.0*phi
    a = np.cos(theta)*np.sin(phi)
    b = np.sin(theta)*np.sin(phi)
    c = np.cos(phi)

    nhat = (a*xhat+b*yhat +c*zhat)/(a**2+b**2 + c**2)**0.5
    return nhat

def generate_atom_r(x):
    """
    generate an atom at position (x, 0, 0)
    """
    r_atom = np.array([[x],[0],[0]])
    return r_atom

def linear_chain(d, N):
    """
    generate a linear chain of atoms at positions:
    (1*d,0,0), (2*d,0,0), ..., (N*d, 0, 0)

    """
    r = np.array([generate_atom_r(i*d) for i in range(N)])
    return r

def Get_SR(M):
    """
    Get superradiant state as done in A. Cidrim, et all (2020). 

    That is:
    
    "The superradiant (SR) state in this context, also labeled
    the timed Dicke state [35], can be identified precisely by
    diagonalizing the single-excitation (linear-optics) coupling
    matrix Mij ≡ Γij + iΔij [36–39]: it corresponds to the
    eigenstate whose eigenvalue has the largest real part,
    ΓSR , while its imaginary part corresponds to its energy
    ΔSR with respect to the atomic transition"

    Algorithm:


    1- find eigenvalues and eigenvectors of M (single-excitation coupling matrix )
    2- find index of largest real eigenvalue, this index corresponds to the index of superradiant
    eigenstate
    3- real part of this eigenstate is ΓSR and imaginary part is ΔSR
    4- create SR state: make an Qobj out of superradiant eigenstate



    """


    eigenvalues, eigenvectors = np.linalg.eig(M)
    largest_real_eigval_index = np.where( np.real(eigenvalues) == max(np.real(eigenvalues)))[0][0]
    Gamma_SR, Delta_SR = np.real(eigenvalues[largest_real_eigval_index]), np.imag(eigenvalues[largest_real_eigval_index])
    SR_state = Qobj(eigenvectors[largest_real_eigval_index])

    return eigenvalues, eigenvectors, Gamma_SR, Delta_SR, SR_state






