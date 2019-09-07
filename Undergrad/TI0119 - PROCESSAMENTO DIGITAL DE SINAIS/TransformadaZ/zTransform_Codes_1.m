%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   
%   TI0119 - PROCESSAMENTO DIGITAL DE SINAIS (2019.1 - T01)
%   1º Trabalho Computacional - Transformada Z
% 
%   Author: Otacilio Bezerra Leite Neto
%
%   zTransform_Codes_1.m
%       Esse script contem os códigos utilizados para simular o primeiro
%       sistema e produzir as visualizações apresentadas no relatório.
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clc; clear all; close all;

syms z a
syms H_1(z)

%% Exemplo 1
%% Definicao da Funcao de Transferencia e Extracao dos Polinomios
% Define a funcao de transferencia
H_1(z) = 1 / (1 - a*z^(-1));

% Define um conjunto de valores para o parametro "a"
a_values = [fliplr(-0.25:-0.25:-1.5) 0.25:0.25:1.5];

% Cria um vetor de funcoes de transferencia pra cada parametro
H_1s = subs(H_1(z), a, a_values);

% Separa os numeradores e denominadores de cada funcao
[num, den] = numden(H_1s);

%% Visualizacoes
colors = jet(size(num,2)*2);
for i = 1:size(num,2)
    num_i = sym2poly(num(i));
    den_i = sym2poly(den(i));
    
    figure(1)
    zplane(num_i, den_i); hold on
    lines = findobj(gcf, 'Type', 'line', '-and', 'color', [0 0.4470 0.7410], '-and', 'marker', 'x', '-or', 'marker', 'o');
    set(lines, 'Color', colors(2*i,:));
    set(lines, 'LineWidth', 1.5);
    set(lines, 'MarkerSize', 20);

    
    figure(2)
    [H,w] = freqz(num_i, den_i, 'whole'); 
    
    subplot(2,1,1), plot(w, 20*log10(abs(H)), 'color', colors(2*i,:)); hold on
    subplot(2,1,2), plot(w, 360/(2*pi)*angle(H), 'color', colors(2*i,:)); hold on
end
figure(1), hold off
title("Plano Z"), xlim([min(a_values)-0.5, max(a_values)+0.5])

figname = "report/figs/ex_1_pz";
fig = gcf; fig.PaperPositionMode = 'auto'; 
print('-bestfit', figname, '-dpdf', '-r300')
system("pdfcrop " + figname + ".pdf " + figname + ".pdf");


figure(2), hold off
subplot(2,1,1), xlabel("\omega (rad)"), ylabel("Magnitude (dB)"), xlim([min(w), max(w)])
subplot(2,1,2), xlabel("\omega (rad)"), ylabel("Fase (rad)"), xlim([min(w), max(w)])

figname = "report/figs/ex_1_bode";
fig = gcf; fig.PaperPositionMode = 'auto'; 
print('-bestfit', figname, '-dpdf', '-r300')
system("pdfcrop " + figname + ".pdf " + figname + ".pdf");
