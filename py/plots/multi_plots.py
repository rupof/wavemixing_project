import fnmatch
import os
import numpy as np
from qutip import file_data_read, Qobj
from glob import glob

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
    for i, run in enumerate(paths_array):
        try:
            dat_run = file_data_read(run)
            runs_dat.append(dat_run)
        except Exception as e:
            print(run)
            print(e)
    return runs_dat




def average_of_array_arrays(array):
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
    avg = average_of_array_arrays(runs_txt)
    return avg




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

def get_positions_from_array_of_paths(paths):
    list_of_r = []
    for i in range(len(paths)):
        list_of_r.append(get_positions_from_a_file(paths[i]))
    return list_of_r 

def get_rho_ss_list(N, Omega, Delta, description, rho_ss_parameter, angle = str(25) ,results_path = "../results/"):
    DefaultInfo = f"N{N}_Omega{Omega}_Delta{Delta}_"
    label = results_path+DefaultInfo+description+"_"+  rho_ss_parameter + "/"
    
    paths_array =get_array_of_runs_dat_files(label)
    #hamiltonean_paths_array=get_array_of_runs_dat_files(label, get_hamiltonean=True)
    #c_ops_paths_array=get_array_of_runs_dat_files(label, get_c_ops=True)
    r_paths_array=get_array_of_runs_dat_files(label, get_r=True)
    print("*------------------------------")
    print(r_paths_array)

    array_of_many_rho_ss_files = get_array_of_dat_runs(paths_array)
    #array_of_hamiltonean_files = get_array_of_dat_runs(hamiltonean_paths_array)
    #array_of_c_ops_files = get_array_of_dat_runs(c_ops_paths_array)
    array_of_r_files = get_positions_from_array_of_paths(r_paths_array)


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













