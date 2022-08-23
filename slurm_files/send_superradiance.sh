#!/usr/bin/bash

echo "sleeping"
echo "woke up"


Omega=1.0
#b0=10.0

N=174

for b0_numbers in {10..18..1} #22 36
do
	b0=$( bc -l <<< "scale=2; ${b0_numbers}/1")
	sbatch --array=0-7%3 get_MC_dynamics.sh $Omega $b0 $N
	echo "sending $b0"
	sleep 5
done	



