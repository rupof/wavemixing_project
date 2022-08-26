#!/usr/bin/bash
#SBATCH -J wavemixing            # Identificação do job
#SBATCH -o %j.out                 # Nome do arquivo de saída padrão (%j = ID do JOB)
#SBATCH --mem-per-cpu=64G
#SBATCH --partition=fast

PYTHON_EXEC=/home/user/miniconda/bin/python


# Criando SCRATCH
export SCRATCHDIR=/scratch/$SLURM_JOBID

mkdir -p ${SCRATCHDIR}
mkdir -p $SCRATCHDIR/results
mkdir -p $SCRATCHDIR/py

# ------------------------
pwd

# Copiando py e singularity pro scratch

cp -r ../py/ $SCRATCHDIR


echo "../py/hello.txt $SCRATCHDIR/hello.txt "
#sbcast ../py/hello.txt  $SCRATCHDIR/py/hello.txt

#cat $SCRATCHDIR/py/hello.txt


for dir in /tmp/*/     # list directories in the form "/tmp/dirname/"
do
    dir=${dir%*/}      # remove the trailing "/"
    echo "${dir##*/}"    # print everything after the final "/"
done


for file in ../py/*.py ../py/*.sh ../py/**/*.py ; do
    echo "copying ${file} to $SCRATCHDIR/${file:3} "
    sbcast "${file}" $SCRATCHDIR/${file:3}
done


cat $SCRATCHDIR/py/hello.txt

#cp -r ../singularity/ $SCRATCHDIR

# ----------------------
# Imprimindo programa principal para ver se estamos no lugar certo!
cat $SCRATCHDIR/py/main_subspace.py
                                    
# cat imprime corretamente! estamos no lugar certo
# ----------------------------------

# rodamos programos com singularity usando o mesmo caminho de antes

singularity exec ../singularity/Singularity_wavemixing.simg $PYTHON_EXEC $SCRATCHDIR/py/main_subspace.py 25 0 3 1 0.1 b0_0.1_S_Int_On_testeBASH_t01 1 0.05 0 direct 0

#Erro: /home/user/miniconda/bin/python: can't open file '/scratch/49601/py/main_subspace.py': [Errno 2] No such file or directory
 


pwd

# Copiamos novos resultados para a pasta local
cp -n ${SCRATCHDIR}/results/  ../results
# Erro
# cp: cannot stat './romain_ic/wavemixing_project/slurm_files/scratch/49603/results/': No such file or directory

echo "Simulation complete!!"


# python -c 'from post_processing.local_calculations.get_g2 import * ; get_g2_zero_from_all_available_rho_ss( 6, 1, 3, 0, "b0_3_S_Int_On_testeODE_t01_", 1, 0.05, 0.0, "direct", 0 )'

