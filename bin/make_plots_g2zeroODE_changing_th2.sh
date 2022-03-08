#!/bin/bash

cd ../src

N=$1

python -m post_processing.local_plotting.plot_g2zero $N 0.05 0.0 b0_3_S_Int_On direct
