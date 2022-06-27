#!/bin/bash                                                                                                                             

ang1=25
ang2=205

N=4 #$1
use_b0=1
b0=1.01 #$3
Description=b0_${b0}_V_Int_On_testing_steady_state_foda_avg
interaction=1 #$6
Omega=0.5 #$7
Delta=20 #$8
rho_ss_parameter=direct
tmax=0

echo "N= $N use_b0= $use_b0 b0= $b0 Description= $Description  int= $interaction Omega= $Omega Delta= $Delta"

cd ../src
python MC_steady_state_dynamics.py $ang1 $ang2 $N $use_b0 $b0 $Description  $interaction $Omega $Delta $rho_ss_parameter $tmax






