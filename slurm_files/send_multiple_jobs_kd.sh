#!/bin/bash


angle1=$1
angle2=$2
N=$3
useb0=$4
kd=$5
exc_radius=1 
Description=$7
num_runs=$8


for (( set_number=1; set_number<=$num_runs; set_number++ ))
do
   echo "Sending job angle1=$angle1 angle2=$angle2 N=$N  Description=$Description num_runs=$num_runs "	
   sbatch job_wave.sh $angle1 $angle2 $N $useb0 $kd $exc_radius  $Description $num_runs      
done

