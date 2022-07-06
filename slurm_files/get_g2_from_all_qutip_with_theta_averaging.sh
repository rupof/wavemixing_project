#!/usr/bin/bash
#SBATCH -J wavemixing            # Identificação do job
#SBATCH -o %j.out                 # Nome do arquivo de saída padrão (%j = ID do JOB)
#SBATCH --partition=fast
#SBATCH --mem=8G

PYTHON_EXEC=/home/user/miniconda/bin/python
SINGULARITY_PATH=/home/u758430/romain_ic/wavemixing_project/singularity/Singularity_wavemixing.simg 
RESULTS_PATH=/home/u758430/romain_ic/wavemixing_project/results 



N=7
b0=0.1   #$( bc -l <<< "scale=2; ${SLURM_ARRAY_TASK_ID}/10")
tmax=0

ang1=25
ang2=205
Omega=2
Delta=20
start_index=0

echo $b0
#useb0=1


echo " atoms: $N"

# Criando SCRATCH
export SCRATCHDIR=/tmp/$SLURM_JOBID

mkdir -p ${SCRATCHDIR}

# Copiando py pro scratch
cp -r ../src/ $SCRATCHDIR

cd $SCRATCHDIR/src                                   
# rodamos com singularity usando o mesmo caminho de antes

singularity exec $SINGULARITY_PATH $PYTHON_EXEC -m post_processing.local_calculations.daily_processing.one_run $ang1 $ang2 $N 1 $b0 b0_${b0}_V_Int_On_theta_avg_ 1 $Omega $Delta direct $tmax $start_index


 

# Copiamos novos resultados para a pasta local
cp -n -r ../results/ $RESULTS_PATH 

#Limpamos tmp
rm -r $SCRATCHDIR


echo "Simulation complete!!"


