from helper_functions.other import *
import matplotlib.pyplot as plt
import re
from helper_functions.cloud import *
from helper_functions.operators import *
from file_manager.file_saver import *
from file_manager.visualization_preparation_tools import *
import os
import sys

sys.path.insert(0, os.path.abspath("./post_processing/local_calculations"))
sys.path.insert(0, os.path.abspath("./helper_functions/cloud"))
sys.path.insert(0, os.path.abspath("./file_manager"))
sys.path.insert(0, os.path.abspath("./hamiltonian_builder"))
sys.path.insert(0, os.path.abspath("./correlation"))
sys.path.insert(0, os.path.abspath("./single_and_double_excitations_subspace"))


plt.style.use('tableau-colorblind10')

thetas = np.float32(np.int32(np.linspace(0,360, 91)))
def get_array_of_runs(N, Omega, Delta, b0):
    # description = "full_sh_implementation_avg" #testing_steady_state_foda_avg
    description = "MC_npz_ind_avg"  # testing_steady_state_foda_avg

    results_path = "../results/"
    DefaultInfo = f"N{N}_Omega{Omega}_Delta{Delta}_"
    defaultangle, angle = "25_", "205"
    rho_ss_parameter = "_direct"

    full_description = f"b0_{b0}_S_Int_On_{description}{rho_ss_parameter}"

    # "_"+ defaultangle +angle+ "_"   + rho_ss_parameter + "/"
    label_folder = results_path+DefaultInfo+full_description + "/"
    paths_array = get_array_of_runs_dat_files(
        label_folder)  # all runs for a given phi
    runs_txt = get_array_of_numpy_runs(paths_array, extension_format="npz")

    # paths_array = get_array_of_runs_dat_files(label_folder, get_r = True) #all runs for a given
    # print(paths_array)
    #runs_txt = get_array_of_numpy_runs(paths_array, npy = True)

    return runs_txt


def get_experiments_data(N, Omega, Delta, b0, description, start_index, end_index):
    #G2_MonteCarlo, G2_MonteCarlo_single_excitation = experiments[exp_num][i][0],  experiments[exp_num][i][1]
    #G2_MonteCarlo_same_direction, G2_MonteCarlo_single_excitation_same_direction = experiments[exp_num][i][2], experiments[exp_num][i][3]
    #I_MonteCarlo, I_MonteCarlo_single_excitation = experiments[exp_num][i][4], experiments[exp_num][i][5]
    #I_MonteCarlo_same_direction, I_MonteCarlo_single_excitation_same_direction = experiments[exp_num][i][6], experiments[exp_num][i][7]
    #taulist = experiments[exp_num][i][8]

    results_path = "../results/"
    DefaultInfo = f"N{N}_Omega{Omega}_Delta{Delta}_b0_{b0}_"
    defaultangle, angle = "25_", "205"
    rho_ss_parameter = "_direct"

    full_description = f"S_Int_On_{description}{rho_ss_parameter}"

    #thetas = np.float32(np.int32(np.linspace(0,359, 90)))[:-1]
    #thetas = np.float32(np.int32(np.linspace(0,360, 90)))
    thetas = np.float32(np.int32(np.linspace(0, 360, 91)))

    experiments = np.zeros(
        [end_index-start_index, len(thetas)], dtype="object")
    indices = []
    for run_index in range(start_index, end_index):
        label_folder = results_path+DefaultInfo+full_description + "/"
        paths_array_containing_theta_files = get_array_of_runs_dat_files(
            label_folder)  # all runs for a given phi
        # print(sorted(paths_array_containing_theta_files)[0:90])
        paths_array = [
            run_name for run_name in paths_array_containing_theta_files if "theta" in run_name and f"run{run_index}" in run_name]
        # print(natural_sort(paths_array[:]))
        print(len(paths_array))
        runs_txt = get_array_of_numpy_runs(
            paths_array[:], extension_format="npz")  # all runs for a given phi
        for angle in range(len(thetas)):
            try:
                experiments[run_index-start_index][angle] = runs_txt[angle]
            except Exception as e:
                print("Problem for: " + str(sorted(paths_array)[0]))
                print(e)
    return experiments


#G2_MonteCarlo, G2_MonteCarlo_single_excitation = experiments[exp_num][i][0],  experiments[exp_num][i][1]
    #G2_MonteCarlo_same_direction, G2_MonteCarlo_single_excitation_same_direction = experiments[exp_num][i][2], experiments[exp_num][i][3]
    #I_MonteCarlo, I_MonteCarlo_single_excitation = experiments[exp_num][i][4], experiments[exp_num][i][5]
    #I_MonteCarlo_same_direction, I_MonteCarlo_single_excitation_same_direction = experiments[exp_num][i][6], experiments[exp_num][i][7]
    #taulist = experiments[exp_num][i][8]


def get_G2_MonteCarlo_from_experiment_and_angle(experiments, exp_num, i, double_excitation_dynamics=True):
    if double_excitation_dynamics == True:
        return experiments[exp_num][i]["arr_0"]


def get_G2_MonteCarlo_single_excitation_from_experiment_and_angle(experiments, exp_num, i, double_excitation_dynamics=True):
    if double_excitation_dynamics == True:
        return experiments[exp_num][i]["arr_1"]
    else:
        return experiments[exp_num][i]["arr_0"]


def get_G2_MonteCarlo_same_direction_from_experiment_and_angle(experiments, exp_num, i, double_excitation_dynamics=True):
    if double_excitation_dynamics == True:
        return experiments[exp_num][i]["arr_2"]


def get_G2_MonteCarlo_single_excitation_same_direction_from_experiment_and_angle(experiments, exp_num, i, double_excitation_dynamics=True):
    if double_excitation_dynamics == True:
        return experiments[exp_num][i]["arr_3"]
    else:
        return experiments[exp_num][i]["arr_1"]


def get_I_MonteCarlo_from_experiment_and_angle(experiments, exp_num, i, double_excitation_dynamics=True):
    if double_excitation_dynamics == True:
        return experiments[exp_num][i]["arr_4"]


def get_I_MonteCarlo_single_excitation_from_experiment_and_angle(experiments, exp_num, i, double_excitation_dynamics=True):
    if double_excitation_dynamics == True:
        return experiments[exp_num][i]["arr_5"]
    else:
        return experiments[exp_num][i]["arr_2"]


def get_I_MonteCarlo_same_direction_from_experiment_and_angle(experiments, exp_num, i, double_excitation_dynamics=True):
    if double_excitation_dynamics == True:
        return experiments[exp_num][i]["arr_6"]


def get_I_MonteCarlo_single_excitation_same_direction_from_experiment_and_angle(experiments, exp_num, i, double_excitation_dynamics=True):
    if double_excitation_dynamics == True:
        return experiments[exp_num][i]["arr_7"]
    else:
        return experiments[exp_num][i]["arr_3"]


def get_taulist_from_experiment_and_angle(experiments, exp_num, i, double_excitation_dynamics=True):
    if double_excitation_dynamics == True:
        return experiments[exp_num][i]["arr_8"]
    else:
        return experiments[exp_num][i]["arr_4"]


def get_g2_from_experiment_and_angle(experiments, exp_num, i, double_excitation_dynamics=True):
    if double_excitation_dynamics == True:
        return get_G2_MonteCarlo_from_experiment_and_angle(experiments, exp_num, i, double_excitation_dynamics=True)/get_I_MonteCarlo_from_experiment_and_angle(experiments, exp_num, i, double_excitation_dynamics=True)


def get_averaged_in_theta_g2(experiments, double_excitation_simulation=True, single_excitation=False):
    #thetas = np.float32(np.int32(np.linspace(0,359, 90)))[:-1]
    #thetas = np.float32(np.int32(np.linspace(0,360, 90)))
    #thetas = np.float32(np.int32(np.linspace(0,361, 90)))[1:-2]

    g2_theta_avg_all_configurations = []
    for run_index in range(len(experiments)):
        # double excitation out of double excitation simulations:
        if double_excitation_simulation == True and single_excitation == False:
            G2_theta_avg = np.average([get_G2_MonteCarlo_from_experiment_and_angle(
                experiments, run_index, angle) for angle in range(len(thetas))], axis=0)
            I_theta_avg = np.average(np.array([get_I_MonteCarlo_from_experiment_and_angle(
                experiments, run_index, angle) for angle in range(len(thetas))]))

            g2_theta_avg = G2_theta_avg/I_theta_avg
            g2_theta_avg_all_configurations.append(g2_theta_avg)

            taulist = get_taulist_from_experiment_and_angle(
                experiments, 0, 0, double_excitation_dynamics=True)

        # single excitation out of double excitation simulations:
        elif double_excitation_simulation == True and single_excitation == True:
            G2_theta_avg = np.average([get_G2_MonteCarlo_single_excitation_from_experiment_and_angle(
                experiments, run_index, angle, double_excitation_dynamics=True) for angle in range(len(thetas))], axis=0)
            I_theta_avg = np.average(np.array([get_I_MonteCarlo_single_excitation_from_experiment_and_angle(
                experiments, run_index, angle, double_excitation_dynamics=True) for angle in range(len(thetas))]))

            g2_theta_avg = G2_theta_avg/I_theta_avg
            g2_theta_avg_all_configurations.append(g2_theta_avg)

            taulist = get_taulist_from_experiment_and_angle(
                experiments, 0, 0, double_excitation_dynamics=False)
        else:
            # double_excitation_simulation == False, therefore single_excitation == True

            # single excitation from single excitation simulations
            G2_theta_avg = np.average([get_G2_MonteCarlo_single_excitation_from_experiment_and_angle(
                experiments, run_index, angle, double_excitation_dynamics=False) for angle in range(len(thetas))], axis=0)
            I_theta_avg = np.average(np.array([get_I_MonteCarlo_single_excitation_from_experiment_and_angle(
                experiments, run_index, angle, double_excitation_dynamics=False) for angle in range(len(thetas))]))

            g2_theta_avg = G2_theta_avg/I_theta_avg
            g2_theta_avg_all_configurations.append(g2_theta_avg)

            taulist = get_taulist_from_experiment_and_angle(
                experiments, 0, 0, double_excitation_dynamics=False)

    return taulist, g2_theta_avg_all_configurations


# 333


N_list = [20, 31, 40]
experiments_by_N = []

b0 = 5
Omegas = [0.1, 0.5, 2.0]


cols = [f'$N = {N}$' for N in N_list]
rows = [f"$\Omega = {Omega} \Gamma $" for Omega in Omegas]


#b0s = [0.1,3]
#Omegas = [0.1,0.5]

Delta = 20.0
j = 1
fig = plt.figure(figsize=(10, 7))

for Omega in Omegas:
    for N in N_list:
    # plt.figure(figsize=(7,10))
        description = "MC_npz_ind_d_exc_avg"

        results_path = "../results/"
        DefaultInfo = f"N{N}_Omega{Omega}_Delta{Delta}_"
        defaultangle, angle = "25_", "205"
        rho_ss_parameter = "_direct"

        try:
            experiments_d_and_s = get_experiments_data(
                N=N, Omega=Omega, Delta=Delta, b0=f"{b0:.2f}", description=description, start_index=0, end_index=4)
        except Exception as e:
            print(e)
            print("Error", N, Omega)

        print(N, Omega)


        tf = 5
        # implement get taulist
        taulist, dt = np.linspace(0, tf, 200, retstep=True)



        relative_error_of_each_simulation = []
        #relative_error_of_each_simulation_single_excitation = []
        
        plt.subplot(len(rows),len(cols), j)



        taulist, g2_12_single_excitation_runs_array = get_averaged_in_theta_g2(
                experiments_d_and_s, double_excitation_simulation=True, single_excitation=True)

        taulist, g2_12_double_excitation_runs_array = get_averaged_in_theta_g2(
                experiments_d_and_s, double_excitation_simulation=True, single_excitation=False)

        num_runs =len( g2_12_double_excitation_runs_array)
        print(num_runs)
        print(len(g2_12_single_excitation_runs_array), len(g2_12_single_excitation_runs_array[0]))
        g2_12_single_excitation_avg = np.average(np.reshape(
                g2_12_single_excitation_runs_array, [num_runs, len(taulist)]), axis=0)
        g2_12_double_excitation_avg = np.average(np.reshape(
                g2_12_double_excitation_runs_array, [num_runs, len(taulist)]), axis=0)

        try:
            avg_relative_error = np.average(relative_error(
                np.real(g2_12_single_excitation_avg), np.real(g2_12_double_excitation_avg)))
        except:
            break
            #plt.title(f" Run {l}:"+ r"$<1-g^{(2)}_{MC}/g^{(2)}_{qutip}>$"+ f"= {np.round(avg_relative_error, 2)}. ", loc = "left")
        print("N", N)
        if N == N_list[0]: #if N first column
            plt.ylabel(r"$g^{(2)}(\tau)$")
            print("1column")
        print("omega", Omega)
        if Omega == Omegas[-1]: #if Omega last row
            plt.xlabel(r"$\tau$ [ns]")
            print("last row")
        #plt.ylim(0, 2.5)

        plt.title(f"Error =  {np.round(avg_relative_error, 2)}")

        plt.plot(taulist*26, np.real(g2_12_single_excitation_avg),
                     "--", label=f"S-excitation. ")
        plt.plot(taulist*26, np.real(g2_12_double_excitation_avg), "--",
                     label=f"D-excitation. ")

        plt.axhline(1, color="black", alpha=0.2)
        plt.suptitle(f"$b_0$ = {b0} ")
        plt.ylim(0,5)
        plt.legend()
        j += 1
            #plt.text(0.7, 1.5+0*np.max(np.real(runs_txt[l][:]))*0.80, r"1-excitation error"+ f"= {np.round(avg_relative_error_single_excitation, 2)} \n2-excitation error"+ f"= {np.round(avg_relative_error, 2)}" )
        #plt.suptitle(f"$N$ = {N}, $b_0$ = {b0}, $\Delta = {Delta} \Gamma $, $\Omega = {Omega} \Gamma $ \n Average of individual errors of double-excitation (and single-excitation) approach = {np.round(np.average(relative_error_of_each_simulation), 2)} ({np.round(np.average(relative_error_of_each_simulation_single_excitation), 2)})")
        #plt.suptitle(f"Average of individual errors of double-excitation (and single-excitation) approach = {np.round(np.average(relative_error_of_each_simulation), 2)} ({np.round(np.average(relative_error_of_each_simulation_single_excitation), 2)})")


axes = fig.axes
axes[0].get_shared_y_axes().join(axes[0], *axes[1:])
axes = np.reshape(axes, [len(rows), len(cols)])


pad = 20
for ax, col in zip(axes[0], cols):
    ax.annotate(col, xy=(0.5, 1), xytext=(0, pad),
                xycoords='axes fraction', textcoords='offset points',
                size='large', ha='center', va='baseline')

pad = 7
for ax, row in zip(axes[:, 0], rows):
    ax.annotate(row, xy=(-0.2, 0.5), xytext=(-ax.yaxis.labelpad - pad, 0),
                xycoords=ax.yaxis.label, textcoords='offset points',
                size='large', ha='right', va='center')

plt.tight_layout()
#plt.show()

plt.savefig(
    f"./benchmarking/test_Delta_{Delta}_b0_{b0}_{len(N_list)}x{len(Omegas)}.png", dpi=300)
