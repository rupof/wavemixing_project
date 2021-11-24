#!/bin/bash



#SBATCH --mail-user=robertoflorezablan@estudante.ufscar.br
#SBATCH --mail-type=ALL



#N=$1 useb0=$2 b0=$3 Description=$4 num_runs=$5 interaction=$6 Omega=$7 Delta=$8





cd ../ 


declare -a b0_list=("10000" )
declare -a Omega_list=("0.02" "1" " 2")
declare -a Delta_list=("0" "20")
declare -a Interaction_list=("Off" "On") 

N=7
use_b0=1
num_runs=40


echo "$N $useb0 $num_runs"

for b0_i in "${b0_list[@]}"
do
		for Interaction in "${Interaction_list[@]}"
		do

				#This magic line assigns Off = 0, On=1
				Interaction_value=$((-1 + 10#0$(IFS=$'\n' echo "${Interaction_list[*]}" | grep --line-number --fixed-strings -- "$Interaction" | cut -f1 -d:)))
				Description="b0_${b0_i}_V_Int_${Interaction}"
	

				#configuration 1
				Omega=${Omega_list[2]}
				Delta=${Delta_list[1]}
								
				echo "Sending configuration 1, b0 = $b0_i, Int = $Interaction"
  				echo "$N $use_b0 $b0_i $Description $num_runs $Interaction_value $Omega $Delta "  

				sbatch send_multiple_jobs_b0_full1.sh $N $use_b0 $b0_i $Description $num_runs $Interaction_value $Omega $Delta
			
				#configuration 2
				Omega=${Omega_list[1]}
				Delta=${Delta_list[0]}
				
				echo "Sending configuration 2, b0 = $b0_i, Int = $Interaction"
		
		
				sbatch send_multiple_jobs_b0_full1.sh $N $use_b0 $b0_i $Description $num_runs $Interaction_value $Omega $Delta


				#configuration 3
				Omega=${Omega_list[0]}
				Delta=${Delta_list[0]}
	
				
				
				echo "Sending configuration 3, b0 = $b0_i, Int = $Interaction"
				sbatch send_multiple_jobs_b0_full1.sh $N $use_b0 $b0_i $Description $num_runs $Interaction_value $Omega $Delta
		done
done

:wq


echo "Terminei!"


