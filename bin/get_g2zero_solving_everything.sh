#!/usr/bin/bash
cd ../src

for run in {1..2}; do
  python main_subspace.py 25 0 5 1 0.1 b0_0.1_V_Int_On_testeODE_t01 1 0.05 0 direct 0
done

