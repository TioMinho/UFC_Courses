"""
=========================
Simulação do Robô SCARPA
=========================

Parte 2 -> Cinemática sem Pontos de Controle

"""
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib.animation as animation
from math import *

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

def entrada():
	print("Simulador Robô SCARPA")
	print("Digite os Parâmetros do Robô:")
	theta1 = radians(float(input("Theta1 (em graus): ")))
	theta2 = radians(float(input("Theta2 (em graus): ")))
	d1 = float(input("D1 (0.5-2.5): "))
	print("Opções de visualização:\n1-Apenas os Frames\n2-Apenas os Elos\n3-Ambos")
	op = int(input("Sua opção: "))
	return(theta1,theta2,d1,op)


def simula():
	################ Criando os Frames  ###########################
	"""
	Observação: Os frames aqui são tratados como três vetores separados e cada vetor
	possui duas triplas:
	(1)-> Posições Pares: Localização do Vetor
	(2)-> Posições Ímpares: Magnitudes nos Eixos

	Assim, para os arrays abaixo teríamos, [0,1]->eixo z, [2,3]->eixo y, [4,5]->eixo z
	"""

	frame1 = np.array([[0, 0, 0], [0, 0, 1],
					   [0, 0, 0], [0, 1, 0],
					   [0, 0, 0], [1, 0, 0]])
	frame1 = np.array(frame1,dtype=float)

	frame2 = np.array([[0, 0, 0], [0, 0, 1],
					   [0, 0, 0], [0, 1, 0],
					   [0, 0, 0], [1, 0, 0]])

	frame2 = np.array(frame2,dtype=float)

	frame3 = np.array([[0, 0, 0], [0, 0, 1],
					   [0, 0, 0], [0, 1, 0],
					   [0, 0, 0], [1, 0, 0]])

	frame3 = np.array(frame3,dtype=float)

	frame4 = np.array([[0, 0, 0], [0, 0, 1],
					   [0, 0, 0], [0, 1, 0],
					   [0, 0, 0], [1, 0, 0]])

	frame4 = np.array(frame4,dtype=float)
	##################################################################

	####### Parâmetros do Robô e Modo de Visualização ################
	(theta1,theta2,d1,op) = entrada()
	L1 = 3
	L2 = 2
	e1 = 1 #espessura do elo 1

	##################################################################

    ############# Transformação entre Frames #########################

	T_0_1 = np.array([[cos(theta1),-sin(theta1),0, 0],
				      [sin(theta1),cos(theta1),0, 0],
				      [0          ,0          ,1, 0],
	                  [0          ,0          ,0, 1]])

	T_1_2 = np.array([[cos(theta2),-sin(theta2),0,L1],
				      [sin(theta2),cos(theta2),0, 0 ],
				      [0          ,0          ,1, e1],
	                  [0          ,0          ,0, 1]])

	T_2_3 = np.array([[1,0,0,L2],
				      [0,-1,0,0 ],
				      [0,0,-1, 0],
	                  [0,0,0, 1]])

	T_3_4 = np.array([[1,0,0, 0],
				      [0,1,0, 0],
				      [0,0,1,d1],
	                  [0,0,0, 1]])

	transformaFrame(T_0_1,frame1)
	transformaFrame(T_0_1.dot(T_1_2),frame2)
	transformaFrame(T_0_1.dot(T_1_2.dot(T_2_3)),frame3)
	transformaFrame(T_0_1.dot(T_1_2.dot(T_2_3.dot(T_3_4))),frame4)

	X = np.concatenate((frame1[::2,0],frame2[::2,0],frame3[::2,0],frame4[::2,0]))
	Y = np.concatenate((frame1[::2,1],frame2[::2,1],frame3[::2,1],frame4[::2,1]))
	Z = np.concatenate((frame1[::2,2],frame2[::2,2],frame3[::2,2],frame4[::2,2]))
	U = np.concatenate((frame1[1::2,0],frame2[1::2,0],frame3[1::2,0],frame4[1::2,0]))
	V = np.concatenate((frame1[1::2,1],frame2[1::2,1],frame3[1::2,1],frame4[1::2,1]))
	W = np.concatenate((frame1[1::2,2],frame2[1::2,2],frame3[1::2,2],frame4[1::2,2]))

	#########################################################################


	############################# Criando o sólido da Base ########################################

	p1 = [0.5,0.5,-3.0]
	p2 = [0.5,-0.5,-3.0]
	p3 = [-0.5,-0.5,-3.0]
	p4 = [-0.5,0.5,-3.0]
	p5 = [0.5,0.5,-0.5]
	p6 = [0.5,-0.5,-0.5]
	p7 = [-0.5,-0.5,-0.5]
	p8 = [-0.5,0.5,-0.5]

	base = np.array([p1,p2,p3,p4,p5,p6,p7,p8])
	vertB = [[base[0],base[1],base[2],base[3]],[base[4],base[5],base[6],base[7]],[base[0],base[4],base[5],base[1]],[base[2],base[6],base[7],base[3]]]

	############################# Criando o sólido do elo 1 #######################################

	p1 = frame1[0]+frame1[3]*0.5+frame1[1]*0.5
	p2 = frame1[0]-frame1[3]*0.5+frame1[1]*0.5
	p3 = frame1[0]-frame1[3]*0.5-frame1[1]*0.5
	p4 = frame1[0]+frame1[3]*0.5-frame1[1]*0.5

	compElo1 = frame1[5]*L1+0.1


	elo1 = np.array([p1,p2,p3,p4,p1+compElo1,p2+compElo1,p3+compElo1,p4+compElo1])
	vert1 = [[elo1[0],elo1[1],elo1[2],elo1[3]],[elo1[4],elo1[5],elo1[6],elo1[7]],[elo1[0],elo1[4],elo1[5],elo1[1]],[elo1[2],elo1[6],elo1[7],elo1[3]]]

	############################# Criando o sólido do elo 2 #######################################

	p1 = frame2[0]+frame2[3]*0.5+frame2[1]*0.5
	p2 = frame2[0]-frame2[3]*0.5+frame2[1]*0.5
	p3 = frame2[0]-frame2[3]*0.5-frame2[1]*0.5
	p4 = frame2[0]+frame2[3]*0.5-frame2[1]*0.5

	compElo2 = frame2[5]*L2+0.1

	elo2 = np.array([p1,p2,p3,p4,p1+compElo2,p2+compElo2,p3+compElo2,p4+compElo2])
	vert2 = [[elo2[0],elo2[1],elo2[2],elo2[3]],[elo2[4],elo2[5],elo2[6],elo2[7]],[elo2[0],elo2[4],elo2[5],elo2[1]],[elo2[2],elo2[6],elo2[7],elo2[3]]]

	############################# Criando o sólido do elo 3 #######################################

	p1 = frame3[0]+frame3[3]*0.2+frame3[5]*0.2
	p2 = frame3[0]-frame3[3]*0.2+frame3[5]*0.2
	p3 = frame3[0]-frame3[3]*0.2-frame3[5]*0.2
	p4 = frame3[0]+frame3[3]*0.2-frame3[5]*0.2
	p5 = frame4[0]+frame4[3]*0.2+frame4[5]*0.2
	p6 = frame4[0]-frame4[3]*0.2+frame4[5]*0.2
	p7 = frame4[0]-frame4[3]*0.2-frame4[5]*0.2
	p8 = frame4[0]+frame4[3]*0.2-frame4[5]*0.2

	elo3 = np.array([p1,p2,p3,p4,p5,p6,p7,p8])
	vert3 = [[elo3[0],elo3[1],elo3[2],elo3[3]],[elo3[4],elo3[5],elo3[6],elo3[7]],[elo3[0],elo3[4],elo3[5],elo3[1]],[elo3[2],elo3[6],elo3[7],elo3[3]]]

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	if(op != 2):
	    ax.quiver(X, Y, Z, U, V, W)

	# Configurações da plotagem
	plt.title("Simulação SCARPA\n")
	ax.view_init(15, -45)
	ax.set_xlim([-5.0, 5.0])
	ax.set_ylim([-5.0, 5.0])
	ax.set_zlim([-4.0, 6.0])
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Z')

	if(op != 1):

	    ax.scatter3D(elo1[:,0],elo1[:,1],elo1[:,2])
	    ax.scatter3D(elo2[:,0],elo2[:,1],elo2[:,2])
	    ax.scatter3D(elo3[:,0],elo3[:,1],elo3[:,2])

	    ax.add_collection3d(Poly3DCollection(vertB, facecolors='black', linewidths=1, edgecolors='r', alpha=.25))
	    ax.add_collection3d(Poly3DCollection(vert1, facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))
	    ax.add_collection3d(Poly3DCollection(vert2, facecolors='lightgreen', linewidths=1, edgecolors='r', alpha=.25))
	    ax.add_collection3d(Poly3DCollection(vert3, facecolors='lightgray', linewidths=1, edgecolors='r', alpha=.25))

	plt.show()

simula()
