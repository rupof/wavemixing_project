#!/bin/bash
cd ../src
N=$1

python -m post_processing.local_plotting.plot_g2zero_b0_changes $N 0.05 0.0 
