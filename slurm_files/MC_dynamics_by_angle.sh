#!/usr/bin/bash
#SBATCH -J wavemixing_MC            # Identificação do job
#SBATCH -o %j.out                 # Nome do arquivo de saída padrão (%j = ID do JOB)
#SBATCH --partition=fast
#SBATCH --mem=4G
PYTHON_EXEC=/home/user/miniconda/bin/python

ang1=${1}
ang2=${2}

N=${3}
use_b0=${4}
b0=${5}
Description=${6} #b0_${b0}_V_Int_On_testing_steady_state_foda_avg
interaction=${7} #$6
Omega=${8} #$7
Delta=${9} #$8
rho_ss_parameter=${10} #direct
tmax=${11}
label_folder=${12}
theta=${13}
single_excitation=${14}
run_id=${15}
steady_state_path=${16}
number_of_angles_total=${17}

echo "label_folder $label_folder"
echo "theta $theta"
echo "single excitation $single_excitation"
echo "run id $run_id"
echo "steady-state path $steady_state_path"
echo "number of angles total $number_of_angles_total"


angles_separation=$((360/$number_of_angles_total))
echo "angles separation $angles_separation"

#path_to_results=
################ Preparing SCRATCH ##############################################


# Criando SCRATCH
export SCRATCHDIR=/tmp/${SLURM_JOB_ID}
mkdir -p ${SCRATCHDIR}


# Copiando py pro scratch
cp -r ../src/ $SCRATCHDIR
#cp get_new_run_number.sh $SCRATCHDIR

##############################################################

#Set the number of runs that each SLURM task should do
PER_TASK=4

# Calculate the starting and ending values for this task based
# on the SLURM task and the number of runs per task.

START_NUM=$(( ($SLURM_ARRAY_TASK_ID - 1) * $PER_TASK + 1 ))
END_NUM=$(( $SLURM_ARRAY_TASK_ID * $PER_TASK ))



START_ANGLE=$(($START_NUM*$angles_separation))
END_ANGLE=$(( $END_NUM*$angles_separation))

# Print the task and run range
echo This is task $SLURM_ARRAY_TASK_ID, which will do runs $START_NUM to $END_NUM. That is angles $START_ANGLE to $END_ANGLE, that are separated by $PER_TASK x $angles_separation

# Run the loop of runs for this task.iiakjdkadj
for (( run=$START_NUM; run<=END_NUM; run++ )); do
  echo This is SLURM task $SLURM_ARRAY_TASK_ID, run number $run and runid $run_id
  theta=$(($run * $angles_separation ))
  echo $theta

  singularity exec ../singularity/Singularity_wavemixing.simg $PYTHON_EXEC $SCRATCHDIR/src/MC_g2_dynamics.py $ang1 $ang2 $N $use_b0 $b0 $Description $interaction $Omega $Delta $rho_ss_parameter $tmax $steady_state_path $theta $single_excitation $SCRATCHDIR $run_id
  #Do your stuff here
done




cp -n -r ${SCRATCHDIR}/results/*  ../results

rm -r ${SCRATCHDIR}/*
