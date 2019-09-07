import numpy as np

def fft(x_n, inverse=False):
	N = len(x_n); 
	W_N = np.exp((-1)**(not inverse) * 2j * np.pi / N)

	x_n = bitrevorder(x_n)

	size = 2
	while size <= N:
		step = size // 2
		for i in range(0, N, size):
			k = 0
			for j in range(i, i + step):
				z_k = (W_N**k) * x_n[j + step]

				x_n[j + step] = x_n[j] - z_k
				x_n[j] 		  = x_n[j] + z_k
				
				k += N // size
		size *= 2

	return (1/N)**inverse * x_n

def shift_fft(X_n):
	N = len(X_n)
	return np.hstack([np.flip(X_n[:(N//2)]), np.flip(X_n[(N//2):])])

def bitrevorder(x):
	N = len(x); size = np.log2(N).astype(int)
	return np.array([x[reverse_bin(i, size)] for i in range(N)], dtype=np.complex_)

def reverse_bin(num, size):
	binary = bin(num)
	reverse = binary[-1:1:-1] 
	reverse = reverse + (size - len(reverse))*'0'

	return int(reverse,2) 

def d_convolve(x, y):
	N = max(len(x), len(y))
	return [sum([x[m]*y[(n-m)%N] for m in range(0,N)]) for n in range(0,N)]

# Radix-4 Decimation-in-Time
def bitrevorder_4(x):
	N = len(x); size = np.log2(np.sqrt(N)).astype(int)
	return np.array([x[0:N-3:4], x[1:N-2:4], x[2:N-1:4], x[3:N:4]]).flatten()

def fft_4(x_n, inverse=False):
	N = len(x_n); 
	W_N = np.exp((-1)**(not inverse) * 2j * np.pi / N)

	x_n = bitrevorder_4(x_n)

	size = 4
	while size <= N:
		step = size // 4
		for i in range(0, N, size):
			k = 0
			for j in range(i, i + step):
				print(size,step,i)
				z1_k = (W_N**(2*k)) * x_n[j + 1*step]
				z2_k = (W_N**k) 	* x_n[j + 2*step]
				z3_k = (W_N**(3*k)) * x_n[j + 3*step]

				
				x_n[j + 2*step] = x_n[j] -1j* z1_k - z2_k +1j * z3_k
				x_n[j + 1*step] = x_n[j] -    z1_k + z2_k - z3_k
				x_n[j + 3*step] = x_n[j] +1j* z1_k - z2_k -1j * z3_k
				
				x_n[j] 		  	= x_n[j] +    z1_k + z2_k +     z3_k
				
				k += N // size
		size *= 4

	return (1/N)**inverse * x_n

