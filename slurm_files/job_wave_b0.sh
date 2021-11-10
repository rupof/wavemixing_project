#!/bin/bash
#SBATCH -J wavemixing            # Identificação do job
#SBATCH -o %j.out                 # Nome do arquivo de saída padrão (%j = ID do JOB)
#SBATCH -n 1
#SBATCH -t 4-00:00:00                # Tempo de execução (hh:mm:ss) - 1h30
#SBATCH --mail-user=robertoflorezablan@estudante.ufscar.br
#SBATCH --mail-type=ALL




service=cloud                               # Nome do perfil remoto no rclone
remote_in=hpc/input                         # Pasta no serviço remoto para input
remote_out=hpc/output                       # Pasta no serviço remoto para output
remote_sing=./  # Pasta no serviço remoto para os containers
container_in=/opt/input                     # Pasta no cluster para input
container_out=/opt/output                   # Pasta no cluster para output
local_sing=.                                # Pasta local para o container singularity
local_job="/scratch/job.${SLURM_JOB_ID}"    # Pasta temporária local
local_in="${local_job}/input/"              # Pasta local para arquivos de entrada
local_out="${local_job}/output/"            # Pasta local para arquivos de saída

PYTHON_EXEC=/home/user/miniconda/bin/python

angle1=$1
angle2=$2
N=$3
useb0=$4
b0=$5
Description=$6
num_runs=$7
interaction=$8
Omega=$9
Delta=$10


echo "Running script in /bin ..."
echo " N=$N angle1=$angle1 angle2=$angle2 "
echo "Running simulations..."

singularity exec ../singularity/Singularity_wavemixing.simg $PYTHON_EXEC ../py/main.py $angle1 $angle2 $N $useb0 $b0 $Description $interaction $Omega $Delta
