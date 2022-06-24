using DifferentialEquations, Random, LinearAlgebra,  TensorOperations, DelimitedFiles

@views function doubleExcitation_memoryTuned(du, u, p, t)
    N, G, Ωₗ, Γₗ, Δₗ, dβₖₗ = p
    βₗ = u[1:N]
    βₖₗ = reshape(u[N+1:end], N, N)

    for l = 1:N
        du[l] = (im * Δₗ[l] - Γₗ[l] / 2) * βₗ[l] - 0.5 * im * Ωₗ[l]  # v2
    end
    mul!(du[1:N], G, βₗ) # du[1:N] .= - G*βₗ


    for k = 1:N
        Ωₖ = Ωₗ[k]
        Gₖ = G[k, :]
        βₖ_linha = βₖₗ[k, :]
        βₖ = βₗ[k]
        for l = 1:N
            dβₖₗ[k, l] =
                (im * (Δₗ[k] + Δₗ[l]) - 0.5 * (Γₗ[k] + Γₗ[l])) * βₖₗ[k, l] -
                0.5im * (Ωₗ[l] * βₖ + Ωₗ[k] * βₗ[l]) - dot(G[l, :], βₖ_linha) -
                dot(Gₖ, βₖₗ[:, l])
        end
    end
    du[N+1:end] .= dβₖₗ[:]

    return nothing
end


function doubleExcitation_speedTuned(du, u, p, t)
    N, G, Ωₗ, Γₗ, Δₗ, rightIndex, _temp = p
    βₗ = u[1:N]
    βₖₗ = reshape(u[N+1:end], N, N)

    for l = 1:N
        du[l] = (im * Δₗ[l] - Γₗ[l] / 2) * βₗ[l] - 0.5 * im * Ωₗ[l]
    end
    mul!(du[1:N], G, βₗ)

    @tensor begin
        _temp[k, l] = G[l, m] * βₖₗ[k, m] + G[k, m] * βₖₗ[m, l]
    end

    for k = 1:N
        for l = 1:N
			if (k == l)
                du[N+rightIndex[k, l]] = 0
            else
				du[N+rightIndex[k, l]] =
					(im * (Δₗ[k] + Δₗ[l]) - 0.5 * (Γₗ[k] + Γₗ[l])) * βₖₗ[k, l] -
					0.5im * (Ωₗ[l] * βₗ[k] + Ωₗ[k] * βₗ[l]) + _temp[k, l]
			end
		end
    end

    return nothing
end


#function doubleExcitation_full_speedTuned(du, u, p, t)
#    N, G, Ωₗ, Γₗ, Δₗ, rightIndex, _temp = p
#    βₗ = u[1:N]
#	βₖₗ = reshape(u[N+1:N*N], N, N) # check if N*N works instead of end
#	γₖₗ = reshape(u[N*N+1:end], N, N)
#	
#	#βₗcalculations
#    for l = 1:N
#        du[l] = (im * Δₗ[l] - Γₗ[l] / 2) * βₗ[l] - 0.5 * im * Ωₗ[l]
#    end
#    mul!(du[1:N], G, βₗ)
#
#	#βₖₗcalculations
#    @tensor begin
#        _temp[k, l] = G[l, m] * βₖₗ[k, m] + G[k, m] * βₖₗ[m, l]
#    end
#
#    for k = 1:N
#        for l = 1:N
#			if (k == l)
#                du[N+rightIndex[k, l]] = 0
#            else
#				du[N+rightIndex[k, l]] =
#					(im * (Δₗ[k] + Δₗ[l]) - 0.5 * (Γₗ[k] + Γₗ[l])) * βₖₗ[k, l] -
#					0.5im * (Ωₗ[l] * βₗ[k] + Ωₗ[k] * βₗ[l]) + _temp[k, l]
#			end
#		end
#    end
#	#γₖₗ
#	@tensor begin
#			_temp[k, l] = G[k, m] * γₖₗ[m, l] + adjoint(G[l, m]) * γₖₗ[k, m]
#    end
#	for k = 1:N
#        for l = 1:N
#			if (k == l)
#                du[N*N+rightIndex[k, l]] = 0
#            else
#				du[N*N+rightIndex[k, l]] =
#					(im * (Δₗ[k] - Δₗ[l]) - 0.5 * (Γₗ[k] + Γₗ[l])) * γₖₗ[k, l] -
#					0.5im * (  Ωₗ[k] * adjoint(βₗ[l]) - adjoint(Ωₗ[l]) * βₗ[k])  + _temp[k, l]
#			end
#		end
#    end
#
#    return nothing
#end
#
function benchmark_test(p)
		N, G, Ωₗ, Γₗ, Δₗ = p
		println(p)
		#G = rand(ComplexF64, N, N);
		G[diagind(G)] .= 0 # avoid the case "m ≠ l"  for dot product
		G .= -G  # avoid an extra operation of negative ("-") inside the TensorOperations

		#Ωₗ = rand(ComplexF64, N)
		#Γₗ = rand(ComplexF64, N)
		#Δₗ = rand(N)
		rightIndex = LinearIndices(G)
		_temp = similar(G)


		p_memory = N, G, Ωₗ, Γₗ, Δₗ, _temp
		p_speed = N, G, Ωₗ, Γₗ, Δₗ, rightIndex, _temp

		u0 = rand(ComplexF64, N + N^2)*0

		prob_memory = ODEProblem(doubleExcitation_memoryTuned, u0, (0.0, 50.0), p_memory)
		prob_speed = ODEProblem(doubleExcitation_speedTuned, u0, (0.0, 50.0), p_speed)

		#sol_memory  = solve(prob_memory, saveat=0.05) #
		sol_speed   = solve(prob_speed, saveat=0.05)
		sol = sol_speed

		t  = sol.t
		#print(length(t))

		β_full = sol.u
        β_full = reduce(hcat,β_full)


		#print(length(βₗ))
		#βₖₗ = [reshape(sol.u[i][N+1:end], N, N) for i in 1:length(sol.u)]

			 

		#printls(p_memory[:length(p_memory)-1])
		
		
		writedlm("../time_test.csv", t, ",")
		writedlm("../beta_full_test.csv", β_full, ",")
		
		return t, β_full
end


#N = 2
#G = ComplexF64[[0.5 0.5]; [0.5 0.5]]
#Γₗ= ComplexF64[1, 1]
#Ωₗ= Float64[0.1, 0.1 ]
#Δₗ= Float64[20,20 ]
#		
#p = N, G, Ωₗ, Γₗ, Δₗ 
#
#benchmark_test(p)
#






