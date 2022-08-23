#!/usr/bin/bash


#Omega=0.5

#b0=10.0
b0=20.0

#N=521

#for b0 in {20..36} #22 36
#	do sbatch --array=0-1%1 get_MC_dynamics.sh $Omega $b0 $N
#	echo "sending $b0"
#	sleep 20	
#done	



for N_i in {20..100..4} #b0 = 22 36, or 180..500..5       
	do sbatch --array=0-1 get_MC_dynamics.sh 0.1 $b0 $N_i
	echo "sending 0.1 $N_i $b0"
	echo "sleeping 200"
	sleep 200
done	

for Omega in 0.1 0.25 0.5 0.75 1.0 1.25 1.5 1.75 2.0 2.25 2.5 2.75 3.0 3.25 3.5 3.75 4.0 4.25 4.5 4.75 5.0 5.25 5.5 5.75 6.0 
do
for N_i in {20..100..4} #b0 = 22 36, or 180..500..5       
	do sbatch --array=0-1 get_MC_dynamics.sh $Omega $b0 $N_i
	echo "sending $Omega $N_i $b0"
	echo "sleeping $N_i"
	sleep 200
done	
done
