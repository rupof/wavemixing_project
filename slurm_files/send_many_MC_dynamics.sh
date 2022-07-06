#!/usr/bin/bash


Omega=6
N=521

for b0 in {20..36} #22 36
	do sbatch --array=0-1%1 get_MC_dynamics.sh $Omega $b0 $N
	echo "sending $b0"
	sleep 20	
done	
