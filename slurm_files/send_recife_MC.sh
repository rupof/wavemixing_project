#!/usr/bin/bash


Omega=6.0

#N=521

#for b0 in {20..36} #22 36
#	do sbatch --array=0-1%1 get_MC_dynamics.sh $Omega $b0 $N
#	echo "sending $b0"
#	sleep 20	
#done	

b0=30
for N_i in {30..200..10} #b0 = 22 36, or 180..500..5       
	do sbatch --array=0-1%2 get_MC_dynamics.sh $Omega $b0 $N_i
	echo "sending $N_i"
	sleep 100	
done

sleep 200 
for N_i in {200..1000..100} #b0 = 22 36, or 180..500..5       
	do sbatch --array=0-1%2 get_MC_dynamics.sh $Omega $b0 $N_i
	echo "sending $N_i"
	sleep 100	
done
