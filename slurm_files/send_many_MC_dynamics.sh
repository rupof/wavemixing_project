#!/usr/bin/bash


Omega=0.5

#N=521

#for b0 in {20..36} #22 36
#	do sbatch --array=0-1%1 get_MC_dynamics.sh $Omega $b0 $N
#	echo "sending $b0"
#	sleep 20	
#done	

for b0 in 0.1 10 14
do
for N_i in {30..70..10} #b0 = 22 36, or 180..500..5       
	do sbatch --array=0-6%2 get_MC_dynamics.sh $Omega $b0 $N_i
	echo "sending $b0"
	sleep 2	
done	
done
