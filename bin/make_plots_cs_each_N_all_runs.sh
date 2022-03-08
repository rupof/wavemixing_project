#!/bin/bash


cd ../src

echo "r1"
declare -a N_list=("1" "2" "3" "4" "5" "6" "$N_i"   )



for N_i in "${N_list[@]}"

	do

		#Resultado1
		python -m post_processing.local_plotting.plot_cs_name_all_runs $N_i 2 20 b0_0.1_V_Int_On_fixed_ direct
		python -m post_processing.local_plotting.plot_cs_name_all_runs $N_i 2 20 b0_3_V_Int_On_fixed_ direct
		python -m post_processing.local_plotting.plot_cs_name_all_runs $N_i 2 20 b0_5_V_Int_On_fixed_ direct


		echo "r2"
		#Resultado2

		python -m post_processing.local_plotting.plot_cs_name_all_runs $N_i 1 0 b0_0.1_V_Int_On_fixed_ direct
		python -m post_processing.local_plotting.plot_cs_name_all_runs $N_i 1 0 b0_3_V_Int_On_fixed_ direct
		python -m post_processing.local_plotting.plot_cs_name_all_runs $N_i 1 0 b0_5_V_Int_On_fixed_ direct

		echo "r3"
		#Resultado3


		python -m post_processing.local_plotting.plot_cs_name_all_runs $N_i 0.02 0 b0_0.1_V_Int_On_fixed_ direct
		python -m post_processing.local_plotting.plot_cs_name_all_runs $N_i 0.02 0 b0_3_V_Int_On_fixed_ direct
		python -m post_processing.local_plotting.plot_cs_name_all_runs $N_i 0.02 0 b0_5_V_Int_On_fixed_ direct





done






