#!/bin/bash


N=$1
useb0=$2
b0=$3
Description=$4
DefaultAngle=25
angle1=$DefaultAngle
num_runs=$5
interaction=$6
Omega=$7
Delta=$8


echo "N= $N use_b0= $use_b0 b0= $b0 Description= $Description num_runs= $num_runs int= $interaction Omega= $Omega Delta= $Delta"

## declare an array of angles
declare -a arr=("25" "90" "155" "-25" "-90" "205")

## now loop through the above array

echo "Angulo 1: $angle1"
for i in "${arr[@]}"
do

   angle2=$i
   echo "Angulo 2 $angle2"
   echo "runs $num_runs"
   # or do whatever with individual element of the array
   	for (( set_number=1; set_number<=$num_runs; set_number++ ))
                 do
		
                        Descriptionwithangles="${Description}_${angle1}_${angle2}"

                        echo "Descrição: $Descriptionwithangles"
                        echo "Sending job angle1=$angle1 angle2=$angle2 N=$N  Description=$Description num_runs=$num_runs "  
                        
  				
			sbatch job_wave_b0.sh $angle1 $angle2 $N $useb0 $b0 $Descriptionwithangles $num_runs $interaction $Omega $Delta
			
	 done

done

