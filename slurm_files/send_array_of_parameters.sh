#!/bin/bash

angle1=25
angle2=25
useb0=1
b0=0.1
Description=b0_0.1_V_Int_On
num_runs=5
interaction=1
Omega=2
Delta=20
declare -a rho_ss_parameter_list=("manual" "direct" "iterative-gmres" "iterative-lgmres" "iterative-bicgstab" "svd" "eigen" "power" )


N=$1

for rho_ss_parameter in "${rho_ss_parameter_list}"
do
	echo 'sending $rho_ss_parameter' 
	sbatch --array [1-$num_runs] job_wave_b0.sh $angle1 $angle2 $N $useb0 $b0 $Description $num_runs $interaction $Omega $Delta $rho_ss_parameter
done

echo 'job send!'
