"""
=====================================
Simulação do Robô SCARPA Generalizado
=====================================

"""
import warnings
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib.animation as animation
from math import *

warnings.filterwarnings("ignore")

# Aplica a transformação de uma Matriz de Transformação a um Frame
def transformaFrame(matrizTransf, frame):
	#Cada frame é tratado como 6 dados, 3 de localização, 3 de orientação
	(m,n) = frame.shape
	ponto = np.zeros(4)

	translacao = matrizTransf[0:3,3]
	rotacao = matrizTransf[0:3,0:3]

	for i in range (0,m):
		if i%2==0:
			frame[i] = frame[i] + translacao
		else:
			frame[i] = rotacao.dot(frame[i])

# Obtem os parâmetros de Cinemática para uma iteração da simulação
def entrada():
	print("Digite os Parâmetros do Robô:")
	theta1  = radians(float(input("Theta1 (em graus): ")))
	theta2  = radians(float(input("Theta2 (em graus): ")))
	d1 		= float(input("D1 (0.5-2.5): "))

	print("Opções de visualização:\n1-Apenas os Frames\n2-Apenas os Elos\n3-Ambos")
	op = int(input("Sua opção: "))

	return(theta1, theta2, d1, op)

# Retorna a tabela de Denavit-Hartenberg equivalente para 'n' Pontos de Controle
def getDHTable(L1, L2, e1, theta1, theta2, d1, n):
	
	k = n-4; a = 0;	b = 0; c = 0
	dhTable = np.zeros([n, 4])

	while(k > 0):
		if k > 0:   #Teremos a pontos de controle entre J0 e J1
			a += 1; k -= 1
		if k > 0:    #Teremos b pontos de controle entre J1 e J2
			b += 1; k -= 1
		if k > 0:    #Teremos c pontos de controle entre J2 e J3
			c += 1; k -= 1

	j1 = a+1; j2 = j1+(b+1); j3 = j2+(c+1)
	
	dhTable[0] 	 	 = [	0,	   	   0,	 	  0, theta1]
	dhTable[1:j1]	 = [	0,	L1/(a+1),	 	  0,	  0]
	dhTable[j1] 	 = [	0,	L1/(a+1),		 e1, theta2]
	dhTable[j1+1:j2] = [	0,  L2/(b+1),	 	  0,	  0]
	dhTable[j2] 	 = [np.pi,  L2/(b+1),		  0, 	  0]
	dhTable[j2+1:j3] = [	0,	   	   0,  d1/(c+1),	  0]
	dhTable[j3] 	 = [	0,	   	   0,  d1/(c+1),	  0]

	return dhTable

def simula():
	
	while(1):
		
		####### Parâmetros do Robô e Modo de Visualização ################
		print("## Simulador Robô SCARPA ##")
		n = int(input("Digite o Número de Pontos de Controles (mínimo 4): "))
		if(n < 4):
			print("Quantidade de Pontos de Controles é menor que 4! A simulação utilizará apenas 4.")
			n = 4

		############# Obtenção dos Parâmetros da Cinemática #########################
		(theta1_F, theta2_F, d1_F, op) = entrada()
		L1 = 3; L2 = 2; e1 = 1;
		
		##################################################################

		# Animação para o estado inicial (0, 0) -> (Theta1, Theta2)
		it = 0
		for theta1, theta2, d1 in zip(np.linspace(0, theta1_F), np.linspace(0,theta2_F), np.linspace(0,d1_F)):
			it +=1
			############# Transformação entre Frames #########################
			"""
			Observação: Os frames aqui são tratados como três vetores separados e cada vetor
			possui duas triplas:
			(1)-> Posições Pares: Localização do Vetor
			(2)-> Posições Ímpares: Magnitudes nos Eixos

			Assim, para os arrays abaixo teríamos, [0,1]->eixo z, [2,3]->eixo y, [4,5]->eixo x

			Observação2: O tensor "T" corresponde à cada matriz de transformação na forma 
			T[i] -> T^{i-1}_{i}. 
			"""

			# Cria a tabela de Denavit-Hartenberg
			DH_Table = getDHTable(L1, L2, e1, theta1, theta2, d1, n)

			# Cria os tensores para Frames e Matrizes de Transformação
			frame = np.zeros([n, 6, 3])
			T = np.zeros([n, 4, 4])

			# Calcula os valores de cada matriz de transformação com base na tabela de Denavit-Hartebberg
			for i in range(0, n):
				eloInf = DH_Table[i]
				T[i] = np.array([[cos(eloInf[3]), 				 -sin(eloInf[3]), 							0, 				      eloInf[1]],
								 [sin(eloInf[3])*cos(eloInf[0]),  cos(eloInf[3])*cos(eloInf[0]), -sin(eloInf[0]), -sin(eloInf[0])*eloInf[2]],
								 [sin(eloInf[3])*sin(eloInf[0]),  cos(eloInf[3])*sin(eloInf[0]),  cos(eloInf[0]),  cos(eloInf[0])*eloInf[2]],
					             [							  0, 						      0, 			   0, 					     1]])

			# Cria os frames de cada Ponto de Controle a aplica a transformação pela matriz de transformação correspondente
			actualT = np.eye(4)
			for i in range(0,n):
				actualT = np.matmul(actualT, T[i])

				frame[i] = np.array([[0, 0, 0], [0, 0, 1], 
								   	 [0, 0, 0], [0, 1, 0],
								   	 [0, 0, 0], [1, 0, 0]], dtype=float)

				transformaFrame(actualT, frame[i])

			# Cria as variáveis que concatenam todos os eixos dos frames (para a visualização)
			X = frame[0][::2,0];  Y = frame[0][::2,1];  Z = frame[0][::2,2]
			U = frame[0][1::2,0]; V = frame[0][1::2,1]; W = frame[0][1::2,2]
			for i in range(1,n):
				X = np.concatenate([X, frame[i][::2,0]])
				Y = np.concatenate([Y, frame[i][::2,1]])
				Z = np.concatenate([Z, frame[i][::2,2]])
				U = np.concatenate([U, frame[i][1::2,0]])
				V = np.concatenate([V, frame[i][1::2,1]])
				W = np.concatenate([W, frame[i][1::2,2]])
			

			#########################################################################

			############################# Criando o sólido da Base ########################################
			p = np.zeros([8,3])

			p[0] = [ 0.5, 0.5, -3.0]
			p[1] = [ 0.5,-0.5, -3.0]
			p[2] = [-0.5,-0.5, -3.0]
			p[3] = [-0.5, 0.5, -3.0]
			p[4] = [ 0.5, 0.5, -0.5]
			p[5] = [ 0.5,-0.5, -0.5]
			p[6] = [-0.5,-0.5, -0.5]
			p[7] = [-0.5, 0.5, -0.5]

			vertB = [p[0:4],p[4:8],[p[0],p[4],p[5],p[1]],[p[2],p[6],p[7],p[3]]]

			############################# Criando o Sólido do Elo 1 #######################################
			p1 = frame[0][0]+frame[0][3]*0.5+frame[0][1]*0.5
			p2 = frame[0][0]-frame[0][3]*0.5+frame[0][1]*0.5
			p3 = frame[0][0]-frame[0][3]*0.5-frame[0][1]*0.5
			p4 = frame[0][0]+frame[0][3]*0.5-frame[0][1]*0.5

			compElo1 = frame[0][5]*L1+0.1

			elo1 = np.array([p1,p2,p3,p4,p1+compElo1,p2+compElo1,p3+compElo1,p4+compElo1])
			vert1 = [elo1[0:4],elo1[4:8],[elo1[0],elo1[4],elo1[5],elo1[1]],[elo1[2],elo1[6],elo1[7],elo1[3]]]

			############################# Criando o Sólido do Elo 2 #######################################
			j_idx = np.ceil((n-4)/3).astype(int) + 1

			p1 = frame[j_idx][0]+frame[j_idx][3]*0.5+frame[j_idx][1]*0.5
			p2 = frame[j_idx][0]-frame[j_idx][3]*0.5+frame[j_idx][1]*0.5
			p3 = frame[j_idx][0]-frame[j_idx][3]*0.5-frame[j_idx][1]*0.5
			p4 = frame[j_idx][0]+frame[j_idx][3]*0.5-frame[j_idx][1]*0.5

			compElo2 = frame[j_idx][5]*L2+0.1

			elo2 = np.array([p1,p2,p3,p4,p1+compElo2,p2+compElo2,p3+compElo2,p4+compElo2])
			vert2 = [elo2[0:4], elo2[4:8], [elo2[0],elo2[4],elo2[5],elo2[1]],[elo2[2],elo2[6],elo2[7],elo2[3]]]

			############################# Criando o Sólido do Elo 3 #######################################
			j_idx = np.ceil((n-(j_idx-1)-4)/2).astype(int) + j_idx + 1

			p1 = frame[j_idx][0]+frame[j_idx][3]*0.2+frame[j_idx][5]*0.2
			p2 = frame[j_idx][0]-frame[j_idx][3]*0.2+frame[j_idx][5]*0.2
			p3 = frame[j_idx][0]-frame[j_idx][3]*0.2-frame[j_idx][5]*0.2
			p4 = frame[j_idx][0]+frame[j_idx][3]*0.2-frame[j_idx][5]*0.2
			p5 = frame[-1][0]+frame[-1][3]*0.2+frame[-1][5]*0.2
			p6 = frame[-1][0]-frame[-1][3]*0.2+frame[-1][5]*0.2
			p7 = frame[-1][0]-frame[-1][3]*0.2-frame[-1][5]*0.2
			p8 = frame[-1][0]+frame[-1][3]*0.2-frame[-1][5]*0.2

			elo3 = np.array([p1,p2,p3,p4,p5,p6,p7,p8])
			vert3 = [elo3[0:4],elo3[4:8],[elo3[0],elo3[4],elo3[5],elo3[1]],[elo3[2],elo3[6],elo3[7],elo3[3]]]

			############################# Plotando as Visualização Gráficas #######################################
			fig = plt.figure(1)
			plt.clf()
			ax = fig.add_subplot(111, projection='3d')
			
			# Plot dos eixos de cada Frame
			if(op != 2):
				ax.quiver(X, Y, Z, U, V, W)

			# Plot das figuras geométricas de cada elo
			if(op != 1):
				ax.scatter3D(elo1[:,0],elo1[:,1],elo1[:,2])
				ax.scatter3D(elo2[:,0],elo2[:,1],elo2[:,2])
				ax.scatter3D(elo3[:,0],elo3[:,1],elo3[:,2])

				ax.add_collection3d(Poly3DCollection(vertB, facecolors='black', linewidths=1, edgecolors='r', alpha=.25))
				ax.add_collection3d(Poly3DCollection(vert1, facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))
				ax.add_collection3d(Poly3DCollection(vert2, facecolors='lightgreen', linewidths=1, edgecolors='r', alpha=.25))
				ax.add_collection3d(Poly3DCollection(vert3, facecolors='lightgray', linewidths=1, edgecolors='r', alpha=.25))

			# Configurações da plotagem
			plt.title("Simulação SCARPA\nTheta Atual=({0:.1f}, {1:.1f}) | Theta Final=({2:.1f}, {3:.1f})".format(degrees(theta1),degrees(theta2),degrees(theta1_F),degrees(theta2_F)))
			ax.view_init(15, 45)
			ax.set_xlim([-5.0, 5.0])
			ax.set_ylim([-5.0, 5.0])
			ax.set_zlim([-4.0, 6.0])
			ax.set_xlabel('X')
			ax.set_ylabel('Y')
			ax.set_zlabel('Z')

			# Plot (interativo)
			plt.show(block=False)
			plt.pause(.001)

		############################# Condição de Encerramento da Simulação #######################################
		isExit = input("Digite 'C' para fazer outra Simulação ou 'X' para sair: ").lower()
		if(isExit == 'x'):
			break

simula()
