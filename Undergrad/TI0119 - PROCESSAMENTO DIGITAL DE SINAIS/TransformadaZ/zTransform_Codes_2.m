%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   
%   TI0119 - PROCESSAMENTO DIGITAL DE SINAIS (2019.1 - T01)
%   1º Trabalho Computacional - Transformada Z
% 
%   Author: Otacilio Bezerra Leite Neto
%
%   zTransform_Codes_2.m
%       Esse script contem os códigos utilizados para simular o segundo
%       sistema e produzir as visualizações apresentadas no relatório.
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clc; clear all; close all;

syms z a n
syms H_2(z)

%% Exemplo 2
%% Definicao da Funcao de Transferencia e Extracao dos Polinomios
% Define a funcao de transferencia
H_2(z) = (1 - a^n * z^(-n)) / (1 - a*z^(-1));

% Define um conjunto de valores para os parametros "n" e "a"
n_values = 4:2:10;
a_values = [-0.8:0.2:-0.2];

% Cria um vetor de funcoes de transferencia pra cada parametro
H_2s = subs(H_2(z), a, a_values);

%% Visualizacoes
for n_i = n_values
    % Cria um vetor de funcoes de transferencia com "n_i" zeros
    H_2sz = subs(H_2s, n, n_i);
    
    % Separa os numeradores e denominadores de cada funcao
    [num, den] = numden(H_2sz);
    
    % Visualizacao propriamente dita
    colors = jet(size(num,2)*2);
    for i = 1:size(num,2)
        num_i = sym2poly(num(i));
        den_i = sym2poly(den(i));

        figure(1)
        zplane(num_i, den_i); hold on
        lines = findobj(gcf, 'Type', 'line', '-and', 'color', [0 0.4470 0.7410], 'marker', 'o');
        set(lines, 'Color', colors(2*i,:));
        set(lines, 'LineWidth', 1.5);
        set(lines, 'MarkerSize', 20);


        figure(2)
        [H,w] = freqz(num_i, den_i, 'whole'); 

        subplot(2,1,1), plot(w, 20*log10(abs(H)), 'color', colors(2*i,:)); hold on
        subplot(2,1,2), plot(w, 360/(2*pi)*angle(H), 'color', colors(2*i,:)); hold on
    end
    figure(1), hold off
    title("Plano Z"), xlim([-max(abs(a_values))-0.5, max(abs(a_values))+0.5])
    
    figname = "report/figs/ex_3_pz_" + num2str(n_i);
    fig = gcf; fig.PaperPositionMode = 'auto'; 
    print('-bestfit', figname, '-dpdf', '-r300')
    system("pdfcrop " + figname + ".pdf " + figname + ".pdf");


    figure(2)
    subplot(2,1,1), hold off, xlabel("\omega (rad)"), ylabel("Magnitude (dB)"), xlim([min(w), max(w)])
    subplot(2,1,2), hold off, xlabel("\omega (rad)"), ylabel("Fase (rad)"), xlim([min(w), max(w)])

    figname = "report/figs/ex_3_bode_" + num2str(n_i);
    fig = gcf; fig.PaperPositionMode = 'auto'; 
    print('-bestfit', figname, '-dpdf', '-r300')
    system("pdfcrop " + figname + ".pdf " + figname + ".pdf");
end