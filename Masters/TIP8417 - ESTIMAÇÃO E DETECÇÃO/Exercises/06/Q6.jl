using Plots, Plots.Measures
using Distributions, StatsBase
using DSP
using LinearAlgebra, ToeplitzMatrices
using LaTeXStrings

# Aliases --------
R(X) 		  = Array{Float64,2}(Toeplitz(autocov(X, 0:1), autocov(X, 0:1)))
p(X, y) 	  = crosscov(X, y, 0:1)
meshgrid(X,Y) = collect(Iterators.product(X, Y))

# =====================================================================
# Functions --------
# Metodo geral para otimizacao por gradiente descendente 
function gradient(X, y, algorithm="deterministic", η=0.1, it=100, verbose=false)
	# Inicializa aleatoriamente os parametros do equalizador
	#	W(z) = w_0 + w_1 z^(-1)
	w = zeros(2, it+1)

	# Calcula as estatísticas de X e Y
	R_x = R(X); p_xd = p(X, y)

	# Seleciona a função do gradiente de acordo com o algoritmo escolhido
	algorithm = lowercase(algorithm)
	if algorithm == "deterministic"
		∇J = (w_k, k) -> 2*(R_x*w_k - p_xd)
	
	elseif algorithm == "newton"
		∇J = (w_k, k) -> 2*(w_k - R_x^(-1)*p_xd)
	
	elseif algorithm == "lms"
	    ∇J = (w_k, k) -> 2*(X[k+1:-1:k]*(X[k+1:-1:k]'*w_k - y[k+1]))

	elseif algorithm == "lms-normalizada"
	    ∇J = (w_k, k) -> (X[k+1:-1:k]*(X[k+1:-1:k]'*w_k - y[k+1]))/(X[k+1:-1:k]'*X[k+1:-1:k])

	end	

	# ===
	# Otimização da função de custo através do gradiente descendente
	for k = 1:it
		## Atualização
		w[:,k+1] = w[:,k] - η*∇J(w[:,k], rand(2:length(X))-1)
		##

		if(verbose)
			println("# It: ", k, " | w[", k,"]: ", w[:,k+1])
		end
	end
	# ===

	return w
end

# ----------
# Calculo da função de erro para um conjunto de pesos W
function J(X, y, W=[0; 0])
	# Calculo das matrizes de autocovariancia
	R_x = R(X); p_xd = p(X,y); σ_d = std(y)^2;

	Jw = zeros(size(W,2))
	for (i,w) in enumerate(eachcol(W))
		Jw[i] = σ_d - 2w'*p_xd + w'*R_x*w
	end

	return Jw
end

# ----------
# Gera uma superficie de erro centrada em realMin
function errorSurface(X, y, realMin=[0; 0])
	# Calculo das matrizes de autocovariancia
	R_x = R(X); p_xd = p(X,y); σ_d = std(y)^2;

	# Declaracao da funcao de custo
	e(w) = σ_d - 2w'*p_xd + w'*R_x*w

	# Cria um espaco de valores dos parametros
	w_x = Array(-0.4:0.005:0.4).+realMin[1]; w_y = Array(-0.4:0.005:0.4).+realMin[2];
	WW = meshgrid(w_x, w_y)
	
	# Calcula a superficie de erro
	error_surface = zeros(size(WW))
	for (i, w) in enumerate(WW)
		error_surface[i] = e(collect(w))
	end

	return w_x, w_y, (error_surface')
end

# =====================================================================
# Dados e Treino dos Parâmetros ---------
X = rand(Normal(0, 1), 999999)
Z = filt([1; 1.6], [1], X) # ou Z = [1 1.6]' * [X [0; X[:end-1]]]

(w_x, w_y, E_surf) = errorSurface(Z, X, [0.352; -0.1582])

param = [0.150 	07; 
		 0.125 	10; 
		 0.100 	15; 
		 0.075 	25; 
		 0.020 	75];
n_param = size(param, 1); max_it = Int(max(param[:,2]...));

w = [gradient(Z, X, "deterministic", param[i,1], max_it) 
				for i in 1:n_param]

# =====================================================================
# Visualização ---------------
pyplot(leg=true, colorbar=false, widen=false, bg=:white)
colors = [:purple, :orange, :green, :red, :blue]

# Visualização da superficie de erro com os passos do algoritmo
c1 = contour(w_x, w_y, E_surf, fill=false, grid=false)
yaxis!(L"w_2(n)"); xaxis!(L"w_1(n)")

for i in n_param:-1:1
	plot!(w[i][1,:], w[i][2,:], 
				l=(0.8, colors[i]), 
				m=(:star5, 5, colors[i], stroke(0)),
				label="N = $(Int(param[i,2])), η = $(param[i,1])")
end
scatter!([0.352], [-0.1582], 
			m=(5, :xcross, :white, stroke(0.5)), 
			label="Optimal")

# Visualização do valor da função de custo para cada iteração
p1 = plot(leg=false)
xaxis!("Iteration"); yaxis!(L"\mathbb{E} [e^2(n)] \vert_{w}")
for i in n_param:-1:1
	plot!(1:max_it, J(Z,X,w[i][:,1:max_it]), 
			l=(0.8, colors[i]))
end

# Plota as duas figuras unidas
plot(c1, p1, size=(16, 6).*60)
