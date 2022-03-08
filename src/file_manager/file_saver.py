import sys
import pathlib
import os
from qutip import file_data_store
import numpy as np

def get_path_to_save_files(N,Omega,Delta, description, extra_path = "", extra_folder_name = ""):
    """creates a folder, if it does not exit,  in  "../results/{0}/"..
        with name format as N#_Omega#_Delta#_description.
        Optional extra_path allows to other adress at the beginning
     returns path to folder

    """
    folder_name = extra_folder_name  + "N{0}_Omega{2}_Delta{3}_{1}".format(str(N), description, Omega, Delta)
    path_to_folder = extra_path + "../results/{0}/".format(folder_name)
    pathlib.Path(path_to_folder).mkdir(parents=True, exist_ok=True) 
    
    path_to_time_folder = "../results/{0}/time/".format(folder_name)
    pathlib.Path(path_to_time_folder).mkdir(parents=True, exist_ok=True) 
    


    path_to_r_folder = "../results/{0}/positions/".format(folder_name)
    pathlib.Path(path_to_r_folder).mkdir(parents=True, exist_ok=True)


    return path_to_folder






def get_new_run_number_txt(filename):
    """ example: 
    (get_run_number_txt("t"))
    for t0 in folder returns 1
    """

    i = 0
    while os.path.exists(f"{filename}{i}.txt") or  os.path.exists(f"{filename}{i}.npy"):
        i += 1
    return i

def get_new_run_number_dat(filename):
    """ example: 
    (get_run_number_txt("t"))
    for t0 in folder returns 1
    """

    i = 0
    while os.path.exists(f"{filename}{i}.dat") or  os.path.exists(f"{filename}{i}.npy"):
        i += 1
    return i


def save_params_to_file(variables_string, filename):
    
    file = open(f"{filename}_params.py", "w")
    file.write(variables_string)
    file.close()


def save_rhoss_to_file(variable, filename):
    output_data = np.vstack((variable))   

    #file = open(f"{filename}_{file_description}.py", "w")
    file_data_store(f'{filename}.dat', output_data.T) 

    
def save_Beta1D_to_file(variable, filename):
    np.savez(variable, f"{filename}_Beta1D")
def save_Beta2D_to_file(variable, filename):
    np.savez(variable, f"{filename}_Beta2D")
def save_t_span_to_file(variable, filename):
    np.savez(variable, f"{filename}_tspan")


