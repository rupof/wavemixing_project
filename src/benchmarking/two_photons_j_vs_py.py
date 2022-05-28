from julia import Main
from julia import Random
from julia import Julia

Main.eval("@eval Main import Base.MainInclude: include")
Main.include("../single_and_double_excitations_subspace/single_time_coefficients.jl")

rand_jl = Random.rand



N = 5


G = rand_jl(Random.ComplexF64, N, N);
Omega_l = rand_jl(Random.ComplexF64, N)
Gamma_l = rand_jl(Random.ComplexF64, N)
Delta_l = rand_jl(N)


print(G)

Main.benchmark_test(2)

