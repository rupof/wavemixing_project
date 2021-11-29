#!/bin/bash

angle1=25
angle2=-90
N=8
useb0=1
b0=0.1
Description=b0_0.1_V_Int_On
num_runs=1
interaction=1
Omega=2
Delta=20

sbatch job_wave_b0.sh $angle1 $angle2 $N $useb0 $b0 $Description $num_runs $interaction $Omega $Delta

echo 'job send!'
