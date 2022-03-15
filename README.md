# Collective effects in biphoton generation of a four-wave-mixing process


The generation of biphotons remains an important field of research, as a number of applications require such sources. Some of their properties are fundamental for quantum information processing (boson sampling) and quantum communication (via quantum teleportation). One mechanism that allows for the production of paired photons is four-wave-mixing process (FWM), taking advantage of the  third-order nonlinear susceptibility χ³ effect. FWM processes in cold atomic ensembles have been employed to generate highly quantum-correlated photon pairs for the last fifteen years in several groups, although atomic interactions were typically disregarded. Recent experiments however have shown evidence of collective behavior in these types of systems. 


In this context, we seek to understand the contributions of dipole-dipole interactions in the generation of biphotons. To this end, we propose an ab initio model, where dipole-dipole interactions arise naturally to describe FWM in cold atomic clouds. Our simulations are consistent with recent experimental results and show evidence of collective behavior.    

This repository contains all bash scripts used to send simulations in our local cluster and the whole python program that runs the simulations

## Program structure
(in construction)

This repository is divided in three folders. 

- `-> bin` Contains the bash scripts to simulate systems and plot results 
- `-> slurm_files` slurm scripts to use in HPC cluster
- `-> src` complete python program.


During our research we consider two computing approaches to calculate the state of the system. The exact (using QuTiP) and the subspace (using scipy) approach.


## Examples

#### Exact steady-state:

``` 
cd ./src
python main.py 25 0 8 1 3 b0_3_S_Int_On_time 1 0.05 0 direct 0 # N = 8, b0 = 3, Interaction: 1 (On), Ω = 0.05,  Δ = 0
``` 
Or using the bash script

``` 
cd ./bin
bash test_rho_ss.sh 
# Calculates the **exact** steady-state for the test state and saves it on the ./results folder
# Test state: N = 8, b0 = 3, Interaction: On, Ω = 0.05,  Δ = 0, direct method 
``` 


#### Subspace ODE:

```
cd ./src
python main_subspace.py 25 0 5 1 0.1 b0_0.1_V_Int_On_testeODE_t01 1 0.05 0 direct 0  
# N = 5, b0 = 0.1, Interaction: On, Ω = 0.05, Δ = 0 
```

Or using bash script

```
cd ./bin
bash get_g2zero_solving_everything.sh
```



