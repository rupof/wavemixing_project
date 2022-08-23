#!/bin/bash
#SBATCH -J wavemixing            # Identificação do job
#SBATCH -o %j.out                 # Nome do arquivo de saída padrão (%j = ID do JOB)
#SBATCH -n 1
#SBATCH -t 4-00:00:00                # Tempo de execução (hh:mm:ss) - 1h30
#SBATCH --mail-user=robertoflorezablan@estudante.ufscar.br
#SBATCH --mail-type=ALL
#SBATCH --partition=normal



PYTHON_EXEC=/home/user/miniconda/bin/python

cd ../src

#singularity exec ../singularity/Singularity_wavemixing.simg $PYTHON_EXEC -m post_processing.local_plotting.plot_g2_grid_comparing_single_and_double_for_different_N 

singularity exec ../singularity/Singularity_wavemixing.simg $PYTHON_EXEC -m post_processing.local_plotting.plot_recife_different_N
