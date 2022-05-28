#!/usr/bin/bash
cd ../src

for run in {1..6}; do
  python QRT_dynamics.py 25 205 7 1 0.1 b0_0.1_V_Int_On_Gauss 1 0.5 20 direct 1
done

