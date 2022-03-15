# Collective effects in biphoton generation of a four-wave-mixing process


The generation of biphotons remains an important field of research, as a number of applications require such sources. Some of their properties are fundamental for quantum information processing (boson sampling) and quantum communication (via quantum teleportation). One mechanism that allows for the production of paired photons is four-wave-mixing process (FWM), taking advantage of the  third-order nonlinear susceptibility χ³ effect. FWM processes in cold atomic ensembles have been employed to generate highly quantum-correlated photon pairs for the last fifteen years in several groups, although atomic interactions were typically disregarded. Recent experiments however have shown evidence of collective behavior in these types of systems. 


In this context, we seek to understand the contributions of dipole-dipole interactions in the generation of biphotons. To this end, we propose an ab initio model, where dipole-dipole interactions arise naturally to describe FWM in cold atomic clouds. Our simulations are consistent with recent experimental results and show evidence of collective behavior.    

This repository contains all bash scripts used to send simulations in our local cluster and the whole python program that runs the simulations. During our research we consider two computing strategies to calculate the state of the system. The exact (using QuTiP) and the subspace (using scipy) approach. A short outline of the computer program is given below. 

## Program structure
(in construction)

This repository is divided in three folders. 

- `-> bin` Contains the bash scripts to simulate systems and plot results. 
- `-> slurm_files` slurm scripts to use in HPC cluster.
- `-> src` full python program.


The `-> src` folder can be understood of a part related exclusively to the physics and mathematics of the problem and a part related to computational file management and post-processing implementations. The physics part consists of:

- `-> helper_functions` contain atomic `cloud` generation scripts, QuTiP quantum `operators`, and `interaction` preparators for coupled dipoles model (scalar and vector). 
- `-> correlation` cauchy schwarz and g⁽²⁾(τ) implementations for both subspace and exact approaches. 
- `-> hamiltonean_builder` builds Green's tensor and Hamiltonean for a set of initial conditions (N, kd and exc_radius or b0, Ω, Δ, ... ) or initial set of positions.
- `-> single_and_double_excitations_subspace` implements the ODE of the subspace approach.

The other part consists of:

- `-> file_manager`
- `-> post_processing`


#### Exact implementation

This way, we solve the open quantum system using QuTiP. Overall, for a given set of conditions, the computational procedure is the following:

1.  Calculate the complete Green's tensor (Matrix of matrices) using `hamiltonean_builder.GreensTensor_and_SRstate`, then compute the system Hamiltonean and Lindbladian collapsible operators `c_ops` using `hamiltonean_builder.system_spec_N`
2.  This is enough to calculate the steady-state of the system using `main.py`
3. With a given steady-state we can calculate g⁽²⁾(τ) using `second_order_correlation.g2_l`

#### Subspace implementation

1.
2.
3.

#### File managing 





## Examples

### Jupyter notebooks:





### Using the terminal:

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


### Using HPC: 
