%%
x = [ones(1,6) zeros(1,58)];

X2 = fft(x);
X = fft_4(x, true);


figure;
subplot(2,2,1), stem(fftshift(abs(X)))
subplot(2,2,2), stem(fftshift(angle(X)))

subplot(2,2,3), stem(fftshift(abs(X2)))
subplot(2,2,4), stem(fftshift(angle(X2)))

function X = fft_4(x, inverse)
    % This is a radix-N FFT, using decimation in frequency
    N = length(x); M = log2(N)/(4/2);
 
    % Initialize variables for floating point sim
    X = complex(zeros(1,N));
    
    % FFT algorithm
    X_aux = x;
    for stage = 0:M-1
        for n=1:N/4
            X((1:4)+(n-1)*4) = radix_dif_bfly(X_aux(n:N/4:end), ... 
                                                  floor((n-1)/(4^stage)) *(4^stage), ... 
                                                  N, ...
                                                  inverse);
        end
        
        X_aux = X;
    end
    
    X = bitrevorder(X*N);
end

function Z = radix_dif_bfly(x, segment, N, inverse)
    A = (1/4) * x(1:4).';
    
    B = (exp(-1j*pi/2)) .^ ((0:4-1)' * (0:4-1)); 
    B = B(bitrevorder(1:4), :);
    
    if(inverse)
        W_aux = ((exp(2j*pi/N)) .^ (bitrevorder(0:4-1)*segment)).';
    else
        W_aux = ((exp(-2j*pi/N)) .^ (bitrevorder(0:4-1)*segment)).';
    end
    
    Z = (B * A) .* W_aux;
end
