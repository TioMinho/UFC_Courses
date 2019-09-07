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
	theta3	= radians(float(input("Theta3 (em graus): ")))

	print("Opções de visualização:\n1-Apenas os Frames\n2-Apenas os Elos\n3-Ambos")
	op = int(input("Sua opção: "))

	return(theta1, theta2, theta3, op)

def simula():
	
	while(1):
		
		####### Parâmetros do Robô e Modo de Visualização ################
		print("## Simulador Robô 3R ##")
		(theta1_F, theta2_F, theta3_F, op) = entrada()
		L1 = 3; L2 = 3; L3 = 2;
		
		##################################################################

		# Animação para o estado inicial (0, 0, 0) -> (Theta1, Theta2, Theta3)
		it = 0
		for theta1, theta2, theta3 in zip(np.linspace(0, theta1_F), np.linspace(0,theta2_F), np.linspace(0,theta3_F)):
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
			DH_Table = np.array([[0, 0,0,theta1],
								 [0,L1,0,theta2],
								 [0,L2,0,theta3]])

			# Cria os tensores para Frames e Matrizes de Transformação
			frame = np.zeros([3, 6, 3])
			T = np.zeros([3, 4, 4])

			# Calcula os valores de cada matriz de transformação com base na tabela de Denavit-Hartebberg
			for i in range(0, 3):
				eloInf = DH_Table[i]
				T[i] = np.array([[cos(eloInf[3]), 				 -sin(eloInf[3]), 							0, 				      eloInf[1]],
								 [sin(eloInf[3])*cos(eloInf[0]),  cos(eloInf[3])*cos(eloInf[0]), -sin(eloInf[0]), -sin(eloInf[0])*eloInf[2]],
								 [sin(eloInf[3])*sin(eloInf[0]),  cos(eloInf[3])*sin(eloInf[0]),  cos(eloInf[0]),  cos(eloInf[0])*eloInf[2]],
					             [							  0, 						      0, 			   0, 					     1]])

			# Cria os frames de cada Ponto de Controle a aplica a transformação pela matriz de transformação correspondente
			actualT = np.eye(4)
			for i in range(0,3):
				actualT = np.matmul(actualT, T[i])

				frame[i] = np.array([[0, 0, 0], [0, 0, 1], 
								   	 [0, 0, 0], [0, 1, 0],
								   	 [0, 0, 0], [1, 0, 0]], dtype=float)

				transformaFrame(actualT, frame[i])

			# Cria as variáveis que concatenam todos os eixos dos frames (para a visualização)
			X = frame[0][::2,0];  Y = frame[0][::2,1];  Z = frame[0][::2,2]
			U = frame[0][1::2,0]; V = frame[0][1::2,1]; W = frame[0][1::2,2]
			for i in range(1,3):
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
			p1 = frame[1][0]+frame[1][3]*0.5+frame[1][1]*0.5
			p2 = frame[1][0]-frame[1][3]*0.5+frame[1][1]*0.5
			p3 = frame[1][0]-frame[1][3]*0.5-frame[1][1]*0.5
			p4 = frame[1][0]+frame[1][3]*0.5-frame[1][1]*0.5

			compElo2 = frame[1][5]*L2+0.1

			elo2 = np.array([p1,p2,p3,p4,p1+compElo2,p2+compElo2,p3+compElo2,p4+compElo2])
			vert2 = [elo2[0:4], elo2[4:8], [elo2[0],elo2[4],elo2[5],elo2[1]],[elo2[2],elo2[6],elo2[7],elo2[3]]]

			############################# Criando o Sólido do Elo 3 #######################################
			p1 = frame[2][0]+frame[2][3]*0.5+frame[2][1]*0.5
			p2 = frame[2][0]-frame[2][3]*0.5+frame[2][1]*0.5
			p3 = frame[2][0]-frame[2][3]*0.5-frame[2][1]*0.5
			p4 = frame[2][0]+frame[2][3]*0.5-frame[2][1]*0.5

			compElo3 = frame[2][5]*L3+0.1

			elo3 = np.array([p1,p2,p3,p4,p1+compElo3,p2+compElo3,p3+compElo3,p4+compElo3])
			vert3 = [elo3[0:4], elo3[4:8], [elo3[0],elo3[4],elo3[5],elo3[1]],[elo3[2],elo3[6],elo3[7],elo3[3]]]

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
			plt.title("Simulação 3R\nTheta: Atual=({0:.1f}, {1:.1f}, {2:.1f}) | Final=({3:.1f}, {4:.1f}, {5:.1f})".format(degrees(theta1),degrees(theta2),degrees(theta3),degrees(theta1_F),degrees(theta2_F),degrees(theta3_F)))
			ax.view_init(15, 45)
			ax.set_xlim([-8.0, 8.0])
			ax.set_ylim([-8.0, 8.0])
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
