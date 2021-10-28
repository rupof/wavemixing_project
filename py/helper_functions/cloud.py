import numpy as np

from  helper_functions.constants import * 

def random_r_i(radius):
    x, y, z = radius*np.random.random(), radius*np.random.random(), radius*np.random.random()
    return np.array([[x],[y],[z]])
    
    
def random_atom(radius):
    r_i = random_r_i(radius)
    r_inorm_square = (r_i.T @ (r_i)).item() 
    while r_inorm_square > radius**2:
        r_i = random_r_i(radius)
        r_inorm_square = (r_i.T @ (r_i)).item() 
    return r_i

def random_cloud(radius, N):
    r = np.array([random_atom(radius) for i in range(N)])
    return r
 
