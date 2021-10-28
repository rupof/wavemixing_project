import sys
import pathlib
import os

def get_path_to_save_files(N,description):
    """creates a folder, if it does not exit,  in  "../results/{0}/"..
        with name format as N#_description
     returns path to folder

    """
    folder_name = "N{0}_{1}".format(str(N), description)
    path_to_folder = "../results/{0}/".format(folder_name)
    pathlib.Path(path_to_folder).mkdir(parents=True, exist_ok=True) 
    return path_to_folder






def get_new_run_number_txt(filename):
    """ example: 
    (get_run_number_txt("t"))
    for t0 in folder returns 1
    """

    i = 0
    while os.path.exists(f"{filename}{i}.txt"):
        i += 1
    return i


def save_params_to_file(variables_string, filename):
    
    file = open(f"{filename}_params.py", "w")
    file.write(variables_string)
    file.close()

