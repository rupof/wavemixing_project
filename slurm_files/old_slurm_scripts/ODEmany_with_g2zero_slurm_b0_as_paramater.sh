#!/usr/bin/bash
#SBATCH -J wavemixing            # Identificação do job
#SBATCH -o %j.out                 # Nome do arquivo de saída padrão (%j = ID do JOB)
#SBATCH --partition=normal
#SBATCH --mem=8G

PYTHON_EXEC=/home/user/miniconda/bin/python


b0=${SLURM_ARRAY_TASK_ID}

echo $b0

N=40


#useb0=1


echo " atoms: $N"

# Criando SCRATCH
export SCRATCHDIR=/tmp/$SLURM_JOBID

mkdir -p ${SCRATCHDIR}

# Copiando py pro scratch
cp -r ../py/ $SCRATCHDIR

                                   
# rodamos com singularity usando o mesmo caminho de antes

singularity exec ../singularity/Singularity_wavemixing.simg $PYTHON_EXEC $SCRATCHDIR/py/main_subspace.py 25 0 $N 1 $b0 b0_${b0}_S_Int_On_changingOD_t01 1 2 20 direct 0


 

# Copiamos novos resultados para a pasta local
cp -n -r ${SCRATCHDIR}/results/  ../results

#Limpamos tmp
rm -r $SCRATCHDIR


echo "Simulation complete!!"


# python -c 'from post_processing.local_calculations.get_g2 import * ; get_g2_zero_from_all_available_rho_ss( 6, 1, 3, 0, "b0_3_S_Int_On_testeODE_t01_", 1, 0.05, 0.0, "direct", 0 )'

