#!/bin/bash

cd ../src

N=$1

#python -m post_processing.local_plotting.plot_g2zero $N 2 20.0 b0_0.1_S_Int_On direct

python -m post_processing.local_plotting.plot_g2zero $N 2 20.0 b0_3_S_Int_On_changingOD_t01 direct
