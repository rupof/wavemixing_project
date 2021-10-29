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
    return np.mean(array,0)
        

def average_of_runs_files(datafolder_path):
    paths_array = get_array_of_runs_files(datafolder_path)
    runs_txt = get_array_of_numpy_runs(paths_array)
    avg = average_of_array_arrays(runs_txt)
    return avg
