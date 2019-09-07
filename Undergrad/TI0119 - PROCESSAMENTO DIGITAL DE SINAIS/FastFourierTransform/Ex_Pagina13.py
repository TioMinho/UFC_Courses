# -- BIBLIOTECAS --
import matplotlib.pyplot as plt
import numpy as np
from FFT import *
import os

# -- INICIALIZAÇÕES --
# Inicialização das sequências x_1[n] e x_2[n]
x1_n = np.array([float(x < 6) for x in range(0, 2**5)])
x2_n = np.array([float(x < 12) for x in range(0, 2**5)])

# Cálculo da Transformadas de Fourier Discretas X_1[k] e X_2[k]
X1_n = fft(x1_n)
X2_n = fft(x2_n)

# Cálculo da multiplicação ponto-a-ponto no domínio da frequência
X_n = X1_n * X2_n

# Cálculo da Transformada Inversa de Fourier do sinal resultante
x_n = fft(X_n, True)

# Cálculo da Transformada Inversa de Fourier utilizando convolução direta no tempo
x_n_r = d_convolve(x1_n, x2_n)

# -- VISUALIZAÇÕES --
# Visualização das sequências no domínio do tempo
plt.figure(figsize=(10, 4)); plt.rc('text', usetex=True)
plt.subplot(1,2,1); plt.stem(x1_n)
plt.ylabel(r'Sinal Discreto - $x_1[n]$', fontsize=12); plt.xlabel(r"Amostra - $[n]$", fontsize=12)
plt.ylim([0, 2])

plt.subplot(1,2,2); plt.stem(x2_n)
plt.ylabel(r'Sinal Discreto - $x_2[n]$', fontsize=12); plt.xlabel(r"Amostra - $[n]$", fontsize=12)
plt.ylim([0, 2])

filename = "report/figs/windows.pdf"
plt.savefig(filename)
os.system("pdfcrop --margins \"0 0 0 0\" \""+filename+"\" \""+filename+"\"")


# Visualização das sequências no domínio da frequência
plt.figure(figsize=(10, 8))
plt.subplot(2,2,1); plt.stem(shift_fft(np.abs(X1_n)))
plt.ylabel(r'Magnitude - $| X_1[n] |$', fontsize=12) 

plt.subplot(2,2,3); plt.stem(shift_fft(np.angle(X1_n)))
plt.ylabel(r'Fase - $\angle X_1[n]$', fontsize=12); plt.xlabel(r"Amostra - $[n]$", fontsize=12)

plt.subplot(2,2,2); plt.stem(shift_fft(np.abs(X2_n)))
plt.ylabel(r'Magnitude - $| X_2[n] |$', fontsize=12)

plt.subplot(2,2,4); plt.stem(shift_fft(np.angle(X2_n)))
plt.ylabel(r'Fase - $\angle X_2[n]$', fontsize=12); plt.xlabel(r"Amostra - $[n]$", fontsize=12)

filename = "report/figs/windowsfft.pdf"
plt.savefig(filename)
os.system("pdfcrop --margins \"0 0 0 0\" \""+filename+"\" \""+filename+"\"")


# Visualização do resultado da multiplicação
plt.figure(figsize=(10, 4))
plt.subplot(1,2,1); plt.stem(shift_fft(np.abs(X_n)))
plt.ylabel(r'Magnitude - $| X_f[n] |$', fontsize=12)

plt.subplot(1,2,2); plt.stem(shift_fft(np.angle(X_n)))
plt.ylabel(r'Fase - $\angle X_f[n]$', fontsize=12)

filename = "report/figs/filterfft.pdf"
plt.savefig(filename)
os.system("pdfcrop --margins \"0 0 0 0\" \""+filename+"\" \""+filename+"\"")


# Visualização da Transformada Inversa sobre o sinal resultante
plt.figure(figsize=(10, 4))
plt.stem(x_n)
plt.ylabel(r'Sinal Discreto - $x_f[n]$', fontsize=12); plt.xlabel(r"Amostra - $[n]$", fontsize=12)

filename = "report/figs/trapez.pdf"
plt.savefig(filename)
os.system("pdfcrop --margins \"0 0 0 0\" \""+filename+"\" \""+filename+"\"")


# Visualização da comparação entre os dois métodos de convolução
plt.figure(figsize=(10, 4))
x = np.arange(0, len(x_n), 1)
plt.plot(x, x_n)
plt.plot(x_n_r, linestyle='--')

plt.ylabel(r'Sinal Discreto - $x_f[n]$', fontsize=12); plt.xlabel(r"Amostra - $[n]$", fontsize=12)
plt.legend(["Convolução por FFT", "Convolução Direta"])

filename = "report/figs/convVsFourier.pdf"
plt.savefig(filename)
os.system("pdfcrop --margins \"0 0 0 0\" \""+filename+"\" \""+filename+"\"")