#!/bin/bash

#N=$1 useb0=$2 b0=$3 Description=$4 num_runs=$5 interaction=$6 Omega=$7 Delta=$8

# Delta=0, Omega = 0.02 No interaction


cd ../ 


declare -a b0_list=("0.1" "3" "5")
declare -a Omega_list=("0.02" "1" " 2")
declare -a Delta_list=("0" "20")
declare -a Interaction_list=("Off" "On") 

N=7
useb0=1
num_runs=40




for b0_i in "${b0_list[@]}"
do
		for Interaction in "${Interaction_list[@]}"
		do

				#This magic line assigns Off = 0, On=1
				Interaction_value=$((-1 + 10#0$(IFS=$'\n' echo "${Interaction_list[*]}" | grep --line-number --fixed-strings -- "$Interaction" | cut -f1 -d:)))
				Description="b0_${b0_i}_V_Int_${Interaction}"
	

				#configuration 1
				$Omega = ${Omega_list[2]}
				$Delta = ${Delta_list[1]}
								
				echo "Sending configuration 1, b0 = $b0_i, Int = $Interaction"
   

				sbatch send_multiple_jobs_b0_full.sh $N $use_b0 $b0_i $Description $num_runs $Interaction_value $Omega $Delta
			
				#configuration 2
				$Omega = ${Omega_list[1]}
				$Delta = ${Delta_list[0]}
				
				echo "Sending configuration 2, b0 = $b0_i, Int = $Interaction"
		
		
				sbatch send_multiple_jobs_b0_full.sh $N $use_b0 $b0_i $Description $num_runs $Interaction_value $Omega $Delta


				#configuration 3
				$Omega = ${Omega_list[0]}
				$Delta = ${Delta_list[0]}
	
				
				
				echo "Sending configuration 3, b0 = $b0_i, Int = $Interaction"
				sbatch send_multiple_jobs_b0_full.sh $N $use_b0 $b0_i $Description $num_runs $Interaction_value $Omega $Delta
		done
done



echo "Terminei!"


