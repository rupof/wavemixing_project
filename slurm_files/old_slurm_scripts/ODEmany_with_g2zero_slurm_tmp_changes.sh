#!/usr/bin/bash
#SBATCH -J wavemixing            # Identificação do job
#SBATCH -o %j.out                 # Nome do arquivo de saída padrão (%j = ID do JOB)
#SBATCH --partition=normal
#SBATCH --mem=8G

PYTHON_EXEC=/home/user/miniconda/bin/python
SINGULARITY_PATH=/home/u758430/romain_ic/wavemixing_project/singularity/Singularity_wavemixing.simg 
RESULTS_PATH=/home/u758430/romain_ic/wavemixing_project/results 


N=$1
b0=$2   #$( bc -l <<< "scale=2; ${SLURM_ARRAY_TASK_ID}/10")
tmax=$3


Omega=0.1
Delta=20


echo $b0
#useb0=1


echo " atoms: $N"
# Criando SCRATCH
export SCRATCHDIR=/tmp/$SLURM_JOBID 

mkdir -p  ${SCRATCHDIR}
mkdir -p  ${SCRATCHDIR}/results


# Copiando py pro scratch
cp -r ../src/ $SCRATCHDIR

cat $SCRATCHDIR/src/QRT_dynamics.py 

TMP_FULL_DIR="$PWD$SCRATCHDIR"                               
# rodamos com singularity usando o mesmo caminho de antes
echo $TMP_FULL_DIR
#cd $SCRATCHDIR 

echo $TMP_FULL_DIR
singularity exec $SINGULARITY_PATH  $PYTHON_EXEC $SCRATCHDIR/src/QRT_dynamics.py 25 0 $N 1 $b0 b0_${b0}_S_Int_On_QRT_t${tmax}_TClusterBravo 1 $Omega $Delta direct $tmax $TMP_FULL_DIR


# Copiamos novos resultados para a pasta local
cp -n -a $SCRATCHDIR/results/  $RESULTS_PATH


#Limpamos tmp
rm -r $SCRATCHDIR


echo "Simulation complete!!"


# python -c 'from post_processing.local_calculations.get_g2 import * ; get_g2_zero_from_all_available_rho_ss( 6, 1, 3, 0, "b0_3_S_Int_On_testeODE_t01_", 1, 0.05, 0.0, "direct", 0 )'

