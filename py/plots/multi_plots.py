import fnmatch
import os
import numpy as np
from qutip import file_data_read, Qobj
from glob import glob
import re
from scipy.stats import gmean
from scipy.stats import hmean

def get_array_of_runs_files(datafolder_path):
    paths_array = []
    for file in os.listdir(datafolder_path):
        if fnmatch.fnmatch(file, '*.txt'):
            paths_array.append(datafolder_path+file)
    return paths_array

def get_array_of_runs_dat_files(datafolder_path, get_hamiltonean = False, get_c_ops = False, get_r = False):
    paths_array = []
    if (get_hamiltonean == False and get_c_ops == False and get_r == False):
        for file in os.listdir(datafolder_path):
            if fnmatch.fnmatch(file, '*.dat'):
                paths_array.append(datafolder_path+file)
        return paths_array
    elif get_c_ops == True:
        for file in os.listdir(datafolder_path+"/c_ops/"):
            if fnmatch.fnmatch(file, 'c_ops*'):
                paths_array.append(datafolder_path+"/c_ops/"+file)
        return paths_array
    elif get_r == True:
        for file in os.listdir(datafolder_path+"/positions/"):
            if fnmatch.fnmatch(file, 'positions*'):
                paths_array.append(datafolder_path+"positions/"+file)
        return paths_array
    elif get_hamiltonean == True:
        for file in os.listdir(datafolder_path+"/hamiltonean/"):
            if fnmatch.fnmatch(file, 'hamiltonean*'):
                paths_array.append(datafolder_path+"/hamiltonean/"+file)
        return paths_array



def get_array_of_numpy_runs(paths_array):
    runs_txt = []
    corrupted_runs = []

    for i, run in enumerate(paths_array):
        try:
            numpy_run = np.loadtxt(run)
            runs_txt.append(numpy_run)
        except Exception as e:
            print(run)
            print(e)

    return runs_txt

def get_array_of_dat_runs(paths_array):
    runs_dat = []
    corrupted_runs = []
    for i, run in enumerate(paths_array):
        try:
            dat_run = file_data_read(run)
            runs_dat.append(dat_run)
        except Exception as e:
            print(e)
            print(run)
            runs_dat.append("error")
            corrupted_runs.append(i)
    return runs_dat, corrupted_runs



def average_of_array_arrays(array, geometric = False):
    if geometric == True:
        try:
            for pair in array:
                pair[0][0] = 0.00000000000000000000000000001
            return gmean(array, 0)
        except Exception as e:
            print(run)
            print(e)

    try:
        return np.mean(array,0)
    except:
        print("array does not exist. Returning 0!")
        return 0
        

def extract_dat_files(datafolder_path):
    "given a datafolder path containing .dat files, returns an array of loaded qutip objects"

    paths_array = get_array_of_runs_files(datafolder_path)
    runs_dat = get_array_of_dat_runs(paths_array)
    return paths_array


def average_of_runs_files(datafolder_path):
    paths_array = get_array_of_runs_files(datafolder_path)
    runs_txt = get_array_of_numpy_runs(paths_array)
    avg = average_of_array_arrays(runs_txt[0:], True)
    return avg


##################################################
#######natural sorting functions:

def atof(text):
    try:
        retval = float(text)
    except ValueError:
        retval = text
    return retval

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    float regex comes from https://stackoverflow.com/a/12643073/190597
    '''
    return [ atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text) ]




################################################################


##Program specific functions

def get_positions_from_a_file(path):
    input_data = file_data_read(path)
    r = []
    for i  in range(0, len(input_data[0]), 3):
        xi = input_data[0][i]
        yi = input_data[0][i+1]
        zi = input_data[0][i+2]
        r_i =np.real( [xi,yi,zi])
        r.append(r_i)
    return r

def get_r_i_path_from_rhoss_i_path(rho_ss_path):
    rho_ss_array_separated_path = rho_ss_path.split("/") 
    # i.e ['..', 'results', 'N6_Omega0.02_Delta0.0_b0_0.1_V_Int_On_fixed_direct', 'N6_Omega0.02_Delta0.0_run13.dat']
    rho_ss_array_separated_path.insert(3, "positions")
    r_i_path = rho_ss_array_separated_path
    #['..', 'results', 'N6_Omega0.02_Delta0.0_b0_0.1_V_Int_On_fixed_direct', 'positions', 'N6_Omega0.02_Delta0.0_run13.dat']    
    r_i_path[4] = "positions_" + r_i_path[4]
    #['..', 'results', 'N6_Omega0.02_Delta0.0_b0_0.1_V_Int_On_fixed_direct', 'positions', 'positions_N6_Omega0.02_Delta0.0_run13.dat']  
    r_i_path_final = "/".join(r_i_path)
    #'../results/N6_Omega0.02_Delta0.0_b0_0.1_V_Int_On_fixed_direct/positions/positions_N6_Omega0.02_Delta0.0_run13'
    return r_i_path_final




def get_positions_and_rhoss_from_array_of_paths(rhoss_paths):
    list_of_r = []
    list_of_rhoss = [] 
    corrupted_runs = []


    for i in range(len(rhoss_paths)):
        #print(rhoss_paths[i])
        r_i_path = get_r_i_path_from_rhoss_i_path(rhoss_paths[i]) 
        try:
            list_of_r.append(get_positions_from_a_file(r_i_path))
            list_of_rhoss.append(file_data_read(rhoss_paths[i]))

        except Exception as e:
            #print("err")
            #print(e)
            corrupted_runs.append(i)
    runs_used =len(rhoss_paths)-len(corrupted_runs) 

    print(f"{len(corrupted_runs)} out of {len(rhoss_paths)} runs where corrupted ({int(len(corrupted_runs)/len(rhoss_paths)*100)}%), we used {runs_used} runs")
    return list_of_rhoss, list_of_r, corrupted_runs 




def get_positions_from_array_of_paths(paths):
    list_of_r = []
    corrupted_runs = []

    for i in range(len(paths)):
        try:
            list_of_r.append(get_positions_from_a_file(paths[i]))
        except Exception as e:
            print(e)
            corrupted_runs.append(i)
            
    return list_of_r, corrupted_runs 


def pop_corrupted_run_from_rho_and_positions(corrupted_indexes, array_of_r_files, array_of_many_rho_ss_files):
    corrupted_indexes = list(corrupted_indexes)
    corrupted_indexes.sort()
    print("Runs left after poppping", len(array_of_many_rho_ss_files)- len(corrupted_indexes))
    print("Corrupted elements", len(corrupted_indexes))
    print(len(array_of_many_rho_ss_files))
    print(corrupted_indexes)
    for counter, i in enumerate(corrupted_indexes):
        print("current_index to pop", i-counter)
        array_of_r_files.pop(i-counter)
        array_of_many_rho_ss_files.pop(i-counter)
        print(len(array_of_r_files))
        print(len(array_of_many_rho_ss_files))
    
    print("Badly formatted and Popped runs: ", counter+1)
    #pop_from_rho


def get_rho_ss_list(N, Omega, Delta, description, rho_ss_parameter, angle = str(25) ,results_path = "../results/"):
    DefaultInfo = f"N{N}_Omega{Omega}_Delta{Delta}_"
    label = results_path+DefaultInfo+description+  rho_ss_parameter + "/"
    
    paths_array =get_array_of_runs_dat_files(label) 
    paths_array.sort(key=natural_keys) 
    array_of_many_rho_ss_files, array_of_r_files, corrupted_runs = get_positions_and_rhoss_from_array_of_paths(paths_array)
 
        

       
    #hamiltonean_paths_array=get_array_of_runs_dat_files(label, get_hamiltonean=True)
    #c_ops_paths_array=get_array_of_runs_dat_files(label, get_c_ops=True)

    #array_of_hamiltonean_files = get_array_of_dat_runs(hamiltonean_paths_array)
    #array_of_c_ops_files = get_array_of_dat_runs(c_ops_paths_array)
    
     



    return array_of_many_rho_ss_files, array_of_r_files 
    





def get_array_of_many_runs_usual_conditions(N, Omega, Delta, DefaultInfo, description, results_path, defaultangle, get_time):
    """
    returns an array that contains 6 arrays (at25_25, at25_90, ... )each of those arrays contains all runs files for that angle.
    
    if get_time, then it also returns a second array that contains 6 arrays (at25_25, at25_90, ... )each of those arrays contains all runs files for time [total_time_ss, total_time_correlation] for that angle.

    """


    angles = [str(25), str(90), str(155), "-"+str(25), "-"+str(90), str(205)]
    
    labels = []
    time_labels = []

    array_of_many_runs = []
    array_of_many_runs_time = []
    


    
    for i, angle in enumerate(angles):
    #  try:
        try:        
            label = results_path+DefaultInfo+description+defaultangle +angle+"/"
            labels.append(label)
            paths_array = get_array_of_runs_files(label)
                    
            array_of_many_runs.append(get_array_of_numpy_runs(paths_array))
            

            time_label = results_path+DefaultInfo+description+defaultangle +angle+"/time/"
            time_labels.append(time_label)
                
            paths_array_time = get_array_of_runs_files(time_label)
            array_of_many_runs_time.append(get_array_of_numpy_runs(paths_array_time))
        except:
            print (label, "does not exist")

            
    try:        
        label = results_path+DefaultInfo+description+"/"
        labels.append(label)
        paths_array = get_array_of_runs_files(label)
                
        array_of_many_runs.append(get_array_of_numpy_runs(paths_array))
        

        time_label = results_path+DefaultInfo+description+ "/time/"
        time_labels.append(time_label)
            
        paths_array_time = get_array_of_runs_files(time_label)
        array_of_many_runs_time.append(get_array_of_numpy_runs(paths_array_time))
    except:
        print (label, "does not exist")

        

    if get_time == True:
        return array_of_many_runs, array_of_many_runs_time
    else:
        return array_of_many_runs













