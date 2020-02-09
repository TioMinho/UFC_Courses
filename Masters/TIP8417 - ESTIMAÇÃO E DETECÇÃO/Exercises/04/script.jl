using Plots, Plots.Measures
using LinearAlgebra
using LaTeXStrings

# Aliases --------
R(X) 		  = Array{Float64,2}(Toeplitz(autocov(X, 0:1), autocov(X, 0:1)))
p(X, y) 	  = crosscov(X, y, 0:1)
meshgrid(X,Y) = collect(Iterators.product(X, Y))

# --
function errorSurface(realMin=[2.0; 4.5])
	# Calculo das matrizes de autocovariancia
	R_x = I(2); p_xd = [2.0; 4.5]; σ_d = 24.40;

	# Declaracao da funcao de custo
	e(w) = σ_d - 2w'*p_xd + w'*R_x*w

	# Cria um espaco de valores dos parametros
	w_x = Array(-5:0.2:5).+realMin[1]; w_y = Array(-5:0.2:5).+realMin[2];
	WW = meshgrid(w_x, w_y)
	
	# Calcula a superficie de erro
	error_surface = zeros(size(WW))
	for (i, w) in enumerate(WW)
		error_surface[i] = e(collect(w))
	end

	return w_x, w_y, (error_surface')
end

(w_x, w_y, E_surf) = errorSurface()

pyplot(leg=true, colorbar=false, widen=false, bg=:white)
s = surface(w_x, w_y, E_surf, zlabel=L"\mathbb{E} [e^2(n)] \vert_{w}")
xaxis!(L"w_1(n)"); yaxis!(L"w_2(n)");

plot(s, size=(8, 6).*60, top_margin=-15pt, right_margin=17pt, left_margin=-30pt)
savefig("figure.pdf")

c = contour(w_x, w_y, E_surf, grid=false)
xaxis!(L"w_1(n)"); yaxis!(L"w_2(n)");

plot(c, size=(6, 6).*60)
savefig("figure2.pdf")
