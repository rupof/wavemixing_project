#!/usr/bin/bash

for run in {1..2}; do
	python main_subspace.py 25 0 6 1 0.1 b0_0.1_S_Int_On_time_t01 1 0.05 0 direct 0
done


# python -c 'from post_processing.local_calculations.get_g2 import * ; get_g2_zero_from_all_available_rho_ss( 6, 1, 3, 0, "b0_3_S_Int_On_testeODE_t01_", 1, 0.05, 0.0, "direct", 0 )'

