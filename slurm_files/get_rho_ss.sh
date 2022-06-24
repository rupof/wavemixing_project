#!/usr/bin/bash
#SBATCH -J wavemixing            # Identificação do job
#SBATCH -o %j.out                 # Nome do arquivo de saída padrão (%j = ID do JOB)
#SBATCH --partition=fast
#SBATCH --mem=8G

PYTHON_EXEC=/home/user/miniconda/bin/python



N=4
b0=0.1   #$( bc -l <<< "scale=2; ${SLURM_ARRAY_TASK_ID}/10")
tmax=0

Omega=2
Delta=20


echo $b0
#useb0=1
extension="dat"

echo " atoms: $N"

# Criando SCRATCH
export SCRATCHDIR=/tmp/$SLURM_JOBID

mkdir -p ${SCRATCHDIR}

# Copiando py pro scratch
cp -r ../src/ $SCRATCHDIR
cp get_new_run_number.sh $SCRATCHDIR

                                   
# rodamos com singularity usando o mesmo caminho de antes

singularity exec ../singularity/Singularity_wavemixing.simg $PYTHON_EXEC $SCRATCHDIR/src/main.py 25 0 $N 1 $b0 b0_${b0}_V_Int_On_TESTE_foda_avg 1 $Omega $Delta direct $tmax $SCRATCHDIR

SCRATCHDIR_results=$SCRATCHDIR/results
size_of_word_to_remove=${#SCRATCHDIR_results}
echo $size_of_word_to_remove

scratch_name_of_file_run=$(echo $SCRATCHDIR/results/*/*run0* )
name_of_file_run=$(echo ${scratch_name_of_file_run:size_of_word_to_remove})

echo run name $name_of_file_run
name_of_file_positions=$(echo $SCRATCHDIR/results/*/positions/*run* )
name_of_file_time=$(echo $SCRATCHDIR}results/*/time/*run* )

name_of_file_run_without_extension=${name_of_file_run%0.${extension}}

echo name $name_of_file_run_without_extension


new_simulation_number=$(bash $SCRATCHDIR/get_new_run_number.sh $name_of_file_run_without_extension dat)
echo "New simulation number" $new_simulation_number
echo $name_of_file_positions

if [ -d "../results/$name_of_file" ]; then
  # if above path exists
	
	new_scratch_name=$SCRATCHDIR_results$name_of_file_run_without_extension${new_simulation_number}.$extension
	mv $scratch_name_of_file_run $new_scratch_name
       	echo $new_scratch_name	


fi

cp -n -r ${SCRATCHDIR}/results/*  ../results


#Limpamos tmp
rm -r $SCRATCHDIR


echo "Simulation complete!!"


