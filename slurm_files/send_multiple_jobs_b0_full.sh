#!/bin/bash


angle1=$1
N=$3
useb0=$4
b0=$5
Description=$6
DefaultAngle=25
num_runs=$7


## declare an array of angles
declare -a arr=("25" "90" "155" "-25" "-90" "205")

## now loop through the above array
for i in "${arr[@]}"
do
   echo "$i"
   angle2=${arr[i]}
   # or do whatever with individual element of the array
	for (( set_number=1; set_number<=$num_runs; set_number++ ))
		 do
			$Descriptionwithangles="${Description}${DefaulAngle}_${angle} " 
			echo "Sending job angle1=$angle1 angle2=$angle2 N=$N  Description=$Description num_runs=$num_runs "  
			sbatch job_wave_b0.sh $angle1 $angle2 $N $useb0 $b0 $Descriptionwithangles $num_runs      
 done
	
done

# You can access them using echo "${arr[0]}", "${arr[1]}" also


for (( set_number=1; set_number<=$num_runs; set_number++ ))
do
   echo "Sending job angle1=$angle1 angle2=$angle2 N=$N  Description=$Description num_runs=$num_runs "	
   sbatch job_wave.sh $angle1 $angle2 $N $useb0 $b0 $Description $num_runs      
done

