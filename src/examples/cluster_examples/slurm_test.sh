#!/usr/bin/bash
#SBATCH -J wavemixing            # Identificação do job
#SBATCH -o %j.out                 # Nome do arquivo de saída padrão (%j = ID do JOB)
#SBATCH --partition=normal
#SBATCH --mem=8G

PYTHON_EXEC=/home/user/miniconda/bin/python



string_input=$1
int_input=$2


# Creating SCRATCH: necessary because SIn UFSCar forces us to do that :(
export SCRATCHDIR=/tmp/$SLURM_JOBID
mkdir -p ${SCRATCHDIR}


# We have to copy our numeric codes to SCRATCH and run the program on that directory
## My numeric codes are in the ../../src/ path
cp -r ../../src/ $SCRATCHDIR

                                   
# We use singularity to invoke cluster python installation and then run the desired file.
## In this case test_cluster.py

singularity exec ../../singularity/Singularity_wavemixing.simg $PYTHON_EXEC $SCRATCHDIR/src/examples/cluster_examples/test_cluster.py ${string_input} ${int_input} 


 

# Copiamos novos resultados para a pasta local
#Necessary in case we are saving simulations in some path:
#cp -n -r ${SCRATCHDIR}/results/  ../results

#We clean scratch
rm -r $SCRATCHDIR


echo "Simulation complete!!"




