#!/bin/bash


cd ../src




N_i=40

python -m post_processing.local_plotting.plot_g2_name $N_i 2 20 b0_0.1_S_Int_On_QRT_ direct



python -m post_processing.local_plotting.plot_g2_name $N_i 2 20 b0_3_S_Int_On_QRT_ direct
python -m post_processing.local_plotting.plot_g2_name $N_i 2 20 b0_5_S_Int_On_QRT_ direct
python -m post_processing.local_plotting.plot_g2_name $N_i 2 20 b0_7_S_Int_On_QRT_ direct


#python -m post_processing.local_plotting.plot_g2_name $N_i 2 20 b0_10_V_Int_On_QRT__ direct

