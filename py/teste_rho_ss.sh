#!/bin/bash
# # ang1(useless) ang2(useless) N useb0 b0 description interaction Omega Delta rho_ss_parameter(useless) tmax(useless)

for run in {1..2}; do
	python main.py 25 0 8 1 3 b0_3_S_Int_On_time 1 0.05 0 direct 0
done
