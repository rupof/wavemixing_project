import numpy as np
from  helper_functions.constants import * 

################################################
#This module is used to calculate everything related to atomic cloud generation
###############################################


def random_number_in_interval(upper_limit, lower_limit):
    return np.random.random()*(upper_limit - lower_limit) + lower_limit


def norm_square(r_i):
    """ Calculates squared norm of a vector """
    return  (r_i.T @ (r_i)).item() 

def check_outside_sphere(r_i, radius):
    """
    Parameters
    -------
    r_i: class: np.array. 
         1x3 vector to check if outside sphere
    radius: float.
        size of atomic cloud
    
    Returns
    ----
    True if r_i is outside of a given radius, False otherwise
    """
    r_inorm_square = norm_square(r_i)
    if r_inorm_square > radius**2:
        return True
    else: 
        return False

def check_outside_exclusion_radius(r_o,r, exc_radius):
    """
    Checks if an atom's position (r_o) is outside of exclusion radius for all atoms in r.

    Parameters
    -------

    r_o: class: np.array. 
        position to be checked
    r: class: np.array.
        array of all atom positions
    exc_radius: float
        minimum distance to other atoms

    Returns
    ----
    True if r_o is outside of a given radius, False otherwise


    """
    for i in range(len(r)):
        distance_square = norm_square(r[i]-r_o) 
        if distance_square > exc_radius**2:
            pass
        else:
            print( "ops, tava dentro!!")
            return False
    return True

def random_r_i(radius):
    """Generates random vector 
    
    Parameters
    -------
    radius: float
        size of maximum possible value of a coordinate
    Returns
    ----------
    random 3d vector (np.array)
    """
    x, y, z = radius*random_number_in_interval(1,-1), radius*random_number_in_interval(1,-1), radius*random_number_in_interval(1,-1)
    return np.array([[x],[y],[z]])
    
    
def random_atom_inside_sphere(radius):
    """
    Generates a random vector inside a sphere of fixed radius:

    """
    r_i = random_r_i(radius)
    while check_outside_sphere(r_i, radius) == True:
        r_i = random_r_i(radius)
       
    return r_i

def random_cloud(radius, N, exc_radius = None, b0 = None):
    """
    Generates an array with 3D vectors, each vector corresponds to a position of an atom
    for a total of N atom. These positions respect each atom's exclusion radius an are 
    inside a sphere of radius "radius". 


    Algorithm:
    1-Determine cloud radius and exclusion radius from a given b0
    2-Create an array of 3d null vectors
    3-For each null vector generate a random position inside the sphere and check if it is
    outside of every atoms exclusion radius. If its not generate new vector.
    4-return array of vectors.
    
    Returns
    -------
    r: array of vector positions for each atom


    """
    if  b0 != None:    #get from  sizes from b0
        print("b0",b0 )
        radius = get_radius_from_optical_thickness(N,b0) 
        exc_radius = get_exclusion_radius_from_optical_thickness(N, radius)

    
    r = np.array([nullvector*(float(i)) for i in range(N)]) 
    for i in range(N):
        r_i = random_atom_inside_sphere(radius)  
        counter = 1 
        while check_outside_exclusion_radius(r_i, r, exc_radius) == False :
            r_i = random_atom_inside_sphere(radius)
            counter += 1
            print(np.sqrt(norm_square(r_i)))
            if counter >20:
                print("Fatal! endless loop")
                break;
        r[i] = r_i # Atom outside exclusion radius and inside sphere  
    return r
   
 
   
   
def get_exclusion_radius_from_optical_thickness(N,kradius):
    """
    for a given k*r determines exclusion radius for each atom given by

    exc_radius = 0.3/rho**(1/3)

    rho is atomic density

    """
    k = 1
    radius = kradius/k
    rho = 4/3*np.pi*radius**3
    exc_radius = 0.3/(rho)**(1/3)
    return exc_radius


def get_radius_from_optical_thickness(N, b0):
    """
    returns atomics radius from optical thickness
    """
    k = 1 
    radius = np.sqrt(2*N/(b0))/k
    return radius

   
   
   
   
   
   
   
