#!/usr/bin/bash
#SBATCH -J ss_FWM            # Identificação do job
#SBATCH -o %j.out                 # Nome do arquivo de saída padrão (%j = ID do JOB)
#SBATCH --partition=normal
#SBATCH --mem=4G

PYTHON_EXEC=/home/user/miniconda/bin/python


############################ Simulation Parameters ###############################
#This parameters are necessary for the physical simulation

ang1=25  #default angles 
ang2=205 #default angles 
N=$3 #$1
use_b0=1
b0=${2}   #$( bc -l <<< "scale=2; ${2}/2") 

interaction=1    #$6
Omega=$1         #$7
Delta=0.0        #$8
rho_ss_parameter=direct
tmax=0
single_excitation=0

################## Implementation Parameters  ####################################
#This parameters describe where to save and how to save the files generated in this simulations
#This can be done much BETTER!!  and it is highly depended on the structure that you implemented to handle the generated files

Description=b0_${b0}_S_Int_On_MC_npz_N_superradiance_exc_avg
results_path=../results/
default_info=N${N}_Omega${Omega}_Delta${Delta}_
label_folder=${results_path}${default_info}${Description}_${rho_ss_parameter}/
label_folder_absolute=/home/u758430/romain_ic/wavemixing_project/results/${default_info}${Description}_${rho_ss_parameter}/


############################ SLURM many angles implementation #################
#These few lines, they are preparing some parameters to compute (40) $num_of_angle polar angle simulations.
#These simulations will perform (3) $PER_TASK angles per job submmited in a total of $total_number_of_task
#I know the notation is terrible! I am very sorry :( 



num_of_angle=40
angle_separation=$((360/$num_of_angle ))
PER_TASK=3
total_distance_between_angles_in_a_task=$(( $PER_TASK * $angle_separation ))

echo "Per Task X angle separation =  $total_distance_between_angles_in_a_task"
total_number_of_task=$((360/($total_distance_between_angles_in_a_task)  ))
echo "Total number of task $total_number_of_task"



################ Preparing SCRATCH ##############################################
#Mandatory procedure due to Cluster Admin policies:
#1. Create a SCRATCH folder (i.e folder in /tmp/ location) where all computations must be performed
#2. Copy python program from src to SCRATCH folder


# making SCRATCH. (1.)
export SCRATCHDIR=/tmp/${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}
mkdir -p ${SCRATCHDIR}
#####
run_id=${SLURM_ARRAY_TASK_ID}

echo "Simulation run_id: $run_id"


# copying src. (2.)
cp -r ../src/ $SCRATCHDIR
cp get_new_run_number.sh $SCRATCHDIR

##############################################################

echo "running steady state"
########## Running Steady State ########################
#Notice we are using SCRATCH

singularity exec ../singularity/Singularity_wavemixing.simg $PYTHON_EXEC $SCRATCHDIR/src/MC_steady_state_dynamics.py $ang1 $ang2 $N $use_b0 $b0 $Description  $interaction $Omega $Delta $rho_ss_parameter $tmax $SCRATCHDIR $run_id

#echo "N= $N use_b0= $use_b0 b0= $b0 Description= $Description  int= $interaction Omega= $Omega Delta= $Delta"

wait

#######################################################################
#Copying steady-states results from SCRATCH to local so that they can be accessed by the dynamics by angle implementation 
cp -n -r ${SCRATCHDIR}/results/*  ../results

wait
sleep 30

#################################################################
## Sending the dynamics by angle with simulations parameters


sbatch --array=0-${total_number_of_task}%50 MC_dynamics_by_angle.sh $ang1 $ang2 $N $use_b0 $b0 $Description $interaction $Omega $Delta $rho_ss_parameter $tmax $label_folder 0 $single_excitation $run_id $label_folder_absolute $num_of_angle





# Cleaning everything :) 

rm -r $SCRATCHDIR/*

echo "Simulation complete!!"
                                
