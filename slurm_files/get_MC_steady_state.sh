#!/bin/bash                                                                                                                             

ang1=${1}
ang2=${2}

N=${3} 
use_b0=${4}
b0=${5}
Description=${6} #b0_${b0}_V_Int_On_testing_steady_state_foda_avg
interaction=${7} #$6
Omega=${8} #$7
Delta=${9} #$8
rho_ss_parameter=${10} direct
tmax=${11}

echo "N= $N use_b0= $use_b0 b0= $b0 Description= $Description  int= $interaction Omega= $Omega Delta= $Delta"

cd ../src
python MC_steady_state_dynamics.py $ang1 $ang2 $N $use_b0 $b0 $Description  $interaction $Omega $Delta $rho_ss_parameter $tmax






