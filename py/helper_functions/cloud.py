import numpy as np

from  helper_functions.constants import * 

def norm_square(r_i):
    return  (r_i.T @ (r_i)).item() 

def check_outside_sphere(r_i, radius):
     r_inorm_square = norm_square(r_i)
     if r_inorm_square > radius**2:
         return True
     else: 
         return False

def check_outside_exclusion_radius(r_o,r, exc_radius):
    """checks if r_i is outside of exclusion radius for all atoms in r
    r_o: position to be checked
    r: array of positions
    exc_radius: exclusion radius
        """
    for i in range(len(r)):
        distance_square = norm_square(r[i]-r_o) 
        if distance_square > exc_radius**2:
            return True
        else:
            return False

def random_r_i(radius):
    x, y, z = radius*np.random.random(), radius*np.random.random(), radius*np.random.random()
    return np.array([[x],[y],[z]])
    
    
def random_atom_inside_sphere(radius):
    r_i = random_r_i(radius)
    while check_outside_sphere(r_i, radius) == True:
        r_i = random_r_i(radius)
       
    return r_i

def random_cloud(exc_radius, radius, N):
    
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
   
 
   
   
   
   
   
   
   
   
   
   
   
   
