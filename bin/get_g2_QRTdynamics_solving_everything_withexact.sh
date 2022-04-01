#!/usr/bin/bash
cd ../src

for run in {1..1}; do
  python QRT_dynamics.py 25 205 7 1 0.1 b0_0.1_V_Int_On_testeQRT_t01 1 2 20 direct 0
done

