#!/usr/bin/bash
#SBATCH -J wavemixing            # Identificação do job
#SBATCH -o %j.out                 # Nome do arquivo de saída padrão (%j = ID do JOB)
#SBATCH --partition=fast
#SBATCH --mem=4G

PYTHON_EXEC=/home/user/miniconda/bin/python


############################ Parameters ###############################
ang1=25
ang2=205

N=$3 #$1
use_b0=1
echo $2
b0=$( bc -l <<< "scale=2; ${2}/2") 
echo "$b0"

Description=b0_${b0}_S_Int_On_MC_npy_ind_avg
interaction=1 #$6
Omega=$1 #$7
Delta=20.0 #$8
rho_ss_parameter=direct
tmax=0


results_path=../results/
default_info=N${N}_Omega${Omega}_Delta${Delta}_
label_folder=${results_path}${default_info}${Description}_${rho_ss_parameter}/

label_folder_absolute=/home/u758430/romain_ic/wavemixing_project/results/${default_info}${Description}_${rho_ss_parameter}/



single_excitation=0
num_of_angle=90
angle_separation=$((360/$num_of_angle ))
PER_TASK=3

total_distance_between_angles_in_a_task=$(( $PER_TASK * $angle_separation ))

echo "Per Task X angle separation =  $total_distance_between_angles_in_a_task"
total_number_of_task=$((360/($total_distance_between_angles_in_a_task)  ))
echo "Total number of task $total_number_of_task"

################ Preparing SCRATCH ##############################################


# Criando SCRATCH
export SCRATCHDIR=/tmp/${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}
mkdir -p ${SCRATCHDIR}
#####
run_id=${SLURM_ARRAY_TASK_ID}

echo "run id $run_id"


# Copiando py pro scratch
cp -r ../src/ $SCRATCHDIR
cp get_new_run_number.sh $SCRATCHDIR

##############################################################

echo "running steady state"
########## Running Steady State ########################

singularity exec ../singularity/Singularity_wavemixing.simg $PYTHON_EXEC $SCRATCHDIR/src/MC_steady_state_dynamics.py $ang1 $ang2 $N $use_b0 $b0 $Description  $interaction $Omega $Delta $rho_ss_parameter $tmax $SCRATCHDIR $run_id

#echo "N= $N use_b0= $use_b0 b0= $b0 Description= $Description  int= $interaction Omega= $Omega Delta= $Delta"

wait
#######################################################################

cp -n -r ${SCRATCHDIR}/results/*  ../results

wait
sleep 30


#sbatch --array=1-10 MC_dynamics_by_angle.sh $ang1 $ang2 $N $use_b0 $b0 $Description $interaction $Omega $Delta $rho_ss_parameter $tmax $label_folder 0 $single_excitation $run_id $label_folder_absolute $num_of_angle

sbatch --array=0-${total_number_of_task}%50 MC_dynamics_by_angle.sh $ang1 $ang2 $N $use_b0 $b0 $Description $interaction $Omega $Delta $rho_ss_parameter $tmax $label_folder 0 $single_excitation $run_id $label_folder_absolute $num_of_angle



#$num_of_angle



#Limpamos tm

rm -r $SCRATCHDIR/*


echo "Simulation complete!!"
                                
