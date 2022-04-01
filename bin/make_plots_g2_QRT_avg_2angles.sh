#!/bin/bash


cd ../src




N_i=40

python -m post_processing.local_plotting.plot_g2_name_just_two_angles_int_on_nice_presentation $N_i 6 20 b0_0.1_S_Int_On_QRT_ direct 0.1



python -m post_processing.local_plotting.plot_g2_name_just_two_angles_int_on_nice_presentation $N_i 6 20 b0_3_S_Int_On_QRT_ direct 3
#python -m post_processing.local_plotting.plot_g2_name_just_two_angles_int_on_nice_presentation $N_i 6 20 b0_5_S_Int_On_QRT_ direct 5
python -m post_processing.local_plotting.plot_g2_name_just_two_angles_int_on_nice_presentation $N_i 6 20 b0_7_S_Int_On_QRT_ direct 7



#python -m post_processing.local_plotting.plot_g2_name $N_i 2 20 b0_10_V_Int_On_QRT__ direct

