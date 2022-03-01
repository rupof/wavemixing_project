#!/usr/bin/bash
cd ../../../

for run in {1..1}; do
  python main_subspace.py 25 0 10 1 0.1 b0_0.1_V_Int_On_testeODE_t01 1 2 20 direct 0
done

