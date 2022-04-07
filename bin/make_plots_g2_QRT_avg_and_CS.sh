#!/bin/bash


cd ../src




N_i=9

#python -m post_processing.local_plotting.plot_g2_name_auto_and_cross_correlation_and_cs $N_i 6 20 b0_0.1_S_Int_On_QRT_ direct 0.1

python -m post_processing.local_plotting.plot_g2_name_auto_and_cross_correlation_and_cs $N_i 2 20 b0_0.1_S_Int_On_QRT_t2_ direct 0.1


python -m post_processing.local_plotting.plot_g2_name_auto_and_cross_correlation_and_cs $N_i 6 20 b0_3_S_Int_On_QRT_ direct 3


python -m post_processing.local_plotting.plot_g2_name_auto_and_cross_correlation_and_cs 30 2 20 b0_3_S_Int_On_QRT_t10 direct 3

python -m post_processing.local_plotting.plot_g2_name_auto_and_cross_correlation_and_cs $N_i 2 20 b0_7_S_Int_On_QRT_ direct 7


python -m post_processing.local_plotting.plot_g2_name_auto_and_cross_correlation_and_cs $N_i 2 20 b0_0.1_S_Int_On_QRT_ direct 0.1

python -m post_processing.local_plotting.plot_g2_name_auto_and_cross_correlation_and_cs $N_i 2 20 b0_3_S_Int_On_QRT_ direct 3


python -m post_processing.local_plotting.plot_g2_name_auto_and_cross_correlation_and_cs $N_i 6 20 b0_7_S_Int_On_QRT_ direct 7


