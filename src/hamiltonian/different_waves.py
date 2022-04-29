import numpy as np

from helper_functions.cloud import norm_square

def get_zR(w0):
    k = 1
    n = 1
    lamb = 2*np.pi/k
    zR = (n*np.pi*w0**2)/lamb
    return zR


def w(z, w0):
    zR = get_zR(w0)
    return w0*np.sqrt(1+ (z/zR)**2 )

def Gouy_phase(z, w0):
    zR = get_zR(w0)
    psi = np.arctan(z/zR) 
    return psi
def wavefront_curvature(z, w0):
    zR = get_zR(w0)
    R  = z * (1+(zR/z)**2)
    return R

def Gaussian_beam(r_i, w0):       
    k = 1
    z = -r_i[2] # We do z -> -z and use wikipedia formula 
    r_square = norm_square(r_i)       
    psi = Gouy_phase(z, w0)
    R = wavefront_curvature(z, w0)

    Gaussian_beam = w0/w(z, w0) * np.exp(-r_square/w(z,w0)**2) *np.exp(-1j*( k*z + k*r_square/(2*R) - psi )  )
    return Gaussian_beam












