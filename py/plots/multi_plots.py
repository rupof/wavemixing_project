import fnmatch
import os
import numpy as np


def get_array_of_runs_files(datafolder_path):
    paths_array = []
    for file in os.listdir(datafolder_path):
        if fnmatch.fnmatch(file, '*.txt'):
            paths_array.append(datafolder_path+file)
    return paths_array

def get_array_of_numpy_runs(paths_array):
    runs_txt = []
    for i, run in enumerate(paths_array):
        numpy_run = np.loadtxt(run)
        runs_txt.append(numpy_run)

    return runs_txt





def average_of_array_arrays(array):
    try:
        return np.mean(array,0)
    except:
        print("array does not exist. Returning 0!")
        return 0
        

def average_of_runs_files(datafolder_path):
    paths_array = get_array_of_runs_files(datafolder_path)
    runs_txt = get_array_of_numpy_runs(paths_array)
    avg = average_of_array_arrays(runs_txt)
    return avg



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













