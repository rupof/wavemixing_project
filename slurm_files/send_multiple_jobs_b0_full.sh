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

## declare an array of angles
declare -a arr=("25" "90" "155" "-25" "-90" "205")

## now loop through the above array
for i in "${arr[@]}"
do
   echo "Angulo2: $i"
   angle2=$i
   # or do whatever with individual element of the array
	for (( set_number=1; set_number<=$num_runs; set_number++ ))
		 do
			$Descriptionwithangles="${Description}${DefaulAngle}_${angle} " 
			echo "Sending job angle1=$angle1 angle2=$angle2 N=$N  Description=$Description num_runs=$num_runs "  
			sbatch job_wave_b0.sh $angle1 $angle2 $N $useb0 $b0 $Descriptionwithangles $num_runs $interaction $Omega $Delta     
 done
	
done

# You can access them using echo "${arr[0]}", "${arr[1]}" also

