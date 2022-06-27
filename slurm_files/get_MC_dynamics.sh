#!/bin/bash                                                                                                                             
ang1=25
ang2=205

N=16 #$1
use_b0=1
b0=1 #$3
Description=b0_${b0}_V_Int_On_testing_steady_state_foda_avg
interaction=1 #$6
Omega=0.5 #$7
Delta=20.0 #$8
rho_ss_parameter=direct
tmax=0

echo "N= $N use_b0= $use_b0 b0= $b0 Description= $Description  int= $interaction Omega= $Omega Delta= $Delta"

cd ../src


python MC_steady_state_dynamics.py $ang1 $ang2 $N $use_b0 $b0 $Description $interaction $Omega $Delta $rho_ss_parameter $tmax


results_path=../results/
default_info=N${N}_Omega${Omega}_Delta${Delta}_
label_folder=${results_path}${default_info}${Description}_${rho_ss_parameter}/

single_excitation=0
num_of_angle=360

angle_separation=$((360/num_of_angle ))
echo $angle_separation
for (( theta=0; theta<=360; theta+= $angle_separation )); do #theta +=3 in cluster 
    echo $theta
	python MC_g2_dynamics.py $ang1 $ang2 $N $use_b0 $b0 $Description $interaction $Omega $Delta $rho_ss_parameter $tmax $label_folder $theta $single_excitation
done

