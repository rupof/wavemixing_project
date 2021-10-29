#!/bin/bash


angle1=$1
angle2=$2
N=$3
Description=$4
num_runs=$5


for (( set_number=1; set_number<=$num_runs; set_number++ ))
do
   echo "Sending job angle1=$angle1 angle2=$angle2 N=$N  Description=$Description num_runs=$num_runs "	
   sbatch job_wave.sh $angle1 $angle2 $N $Description      
done

