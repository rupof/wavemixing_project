#!/bin/bash

echo "começo"

#SBATCH --mail-user=robertoflorezablan@estudante.ufscar.br
#SBATCH --mail-type=ALL
#SBATCH --mem=170G
#SBATCH --output=daily_%j.out
#SBATCH --error=daily_%j.err
#SBATCH --partition=fast


#N=$1 useb0=$2 b0=$3 Description=$4 num_runs=$5 interaction=$6 Omega=$7 Delta=$8





cd ../ 




declare -a N_list=("1" "2" "3" "4" "5" "6" "7" "8"  )





for N_i in "${N_list[@]}"
do	
	send_array_of_parameters.sh $N_i
done 


echo "Terminei!"


