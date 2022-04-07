#!/bin/bash
cd ../src
N=50
b0=1
t=3
Omega=0.5

python -m post_processing.local_plotting.plot_g2_name_auto_and_cross_correlation_and_cs $N $Omega 20 b0_${b0}_S_Int_On_QRT_t${t}_ direct ${b0}

#python -m post_processing.local_plotting.plot_g2_name_auto_and_cross_correlation_and_cs $N 2 20 b0_${b0}_S_Int_On_QRT_ direct ${b0}

