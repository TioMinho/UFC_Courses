%%
% Cria um circuito Ladder Network dado uma Função de Transferência
syms s
poles = 1.68067 * exp(1j*(pi*(1+2*(0:1:13)+14)/(2*14)));
K = abs(prod(-poles));
D_s = vpa(sum(poly(poles) .* s.^(14:-1:0)), 4);

Z11 = vpa(1/((D_s + s^14) / (D_s - s^14)), 4);
[num, den] = numden(Z11);
[qo, re] = quorem(num, den);

vpa(qo, 3)

try 
    while(true)
    Z11 = den/re;
    [num, den] = numden(Z11);
    [qo, re] = quorem(num, den);

    vpa(qo, 3)
    end
catch
   fprintf("fim\n") 
end

%%