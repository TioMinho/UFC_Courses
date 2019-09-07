#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import *
from tkinter import ttk, messagebox

# Classe Aplicação da Aplicação (Interface Gráfica)
class ServerApp(object):
	def __init__(self, master=None):
		# Variáveis da Casa
		self.locations = ["Quarto", "Cozinha", "Banheiro", "Sala", "Entrada", ]

		# Variáveis de Conexão
		self.clients = {}
		self.addresses = {}
		
		self.HOST = ''
		self.PORT = 33000
		self.BUFSIZ = 1024
		self.ADDR = (self.HOST, self.PORT)
		self.SERVER = socket(AF_INET, SOCK_STREAM)
		self.SERVER.bind(self.ADDR)

		self.sensors_text = {}
		self.actuators_text = {}

		self.start_server(15)

		# Variáveis das Interfaces Gráficas
		self.master = master
		self.master.protocol("WM_DELETE_WINDOW", self.leave_server)

		self.tab_control = ttk.Notebook(master)

		self.tab1 = ttk.Frame(self.tab_control)
		self.tab2 = ttk.Frame(self.tab_control)

		self.tab_control.add(self.tab1, text='Sensors')
		self.tab_control.add(self.tab2, text='Actuators')
		
		# Inicialização de Elemento das Tabs
		self.tab1_frames = {}; self.tab2_frames = {}
		for it, loc in enumerate(self.locations):
			# Sensores
			self.tab1_frames[loc] = [ttk.LabelFrame(self.tab1, text=loc, borderwidth=3, relief=RAISED), 0, []]
			self.tab1_frames[loc][0].grid(row=((it//3)+1), column=(it%3)+1, sticky=E+W+N+S, padx=20, pady=10, ipadx=10, ipady=10)
			self.tab1_frames[loc][0].grid_columnconfigure(2, minsize=25)
			for i in range(0,4):
				labelText = StringVar()
				
				tab_text = Label(self.tab1_frames[loc][0], font=("Calibri", "10", "bold"), textvariable=labelText)
				tab_text.grid(row=i+1, column=1, sticky=W)
				
				labelText.set("S:")
				self.tab1_frames[loc][2].append(labelText)

				labelText = StringVar()
				
				tab_text = Label(self.tab1_frames[loc][0], textvariable=labelText)
				tab_text.grid(row=i+1, column=3, sticky=W)
				
				labelText.set("0")
				self.tab1_frames[loc][2].append(labelText)

			# Atuadores
			self.tab2_frames[loc] = [ttk.LabelFrame(self.tab2, text=loc, borderwidth=3, relief=RAISED), 0, []]
			self.tab2_frames[loc][0].grid(row=((it//3)+1), column=(it%3)+1, sticky=E+W+N+S, padx=20, pady=10, ipadx=10, ipady=10)
			self.tab2_frames[loc][0].grid_columnconfigure(2, minsize=25)
			for i in range(0,4):
				labelText = StringVar()
				
				tab_text = Label(self.tab2_frames[loc][0], font=("Calibri", "10", "bold"), textvariable=labelText)
				tab_text.grid(row=(i*2)+1, column=1, columnspan=2, sticky=W)
				
				labelText.set("A:")
				self.tab2_frames[loc][2].append(labelText)

				labelText = StringVar()
				
				tab_text = Label(self.tab2_frames[loc][0], textvariable=labelText)
				tab_text.grid(row=(i*2)+1, column=3, sticky=W)
				
				labelText.set("Off")
				self.tab2_frames[loc][2].append(labelText)

				bt = Button(self.tab2_frames[loc][0], text="▲", width=5)
				bt["command"] = lambda location=loc, idx=i: self.send_command(location,idx,"up")
				bt.grid(row=(i*2)+2, column=1, sticky=E+W+N+S)
				
				bt = Button(self.tab2_frames[loc][0], text="Power", width=5)
				bt["command"] = lambda location=loc, idx=i: self.send_command(location,idx,"power")
				bt.grid(row=(i*2)+2, column=2, sticky=E+W+N+S)

				bt = Button(self.tab2_frames[loc][0], text="▼", width=5)
				bt["command"] = lambda location=loc, idx=i: self.send_command(location,idx,"down")
				bt.grid(row=(i*2)+2, column=3, sticky=E+W+N+S)

		self.tab_control.pack(expand=1, fill='both')
		
	# Método de Inicialização do Servidor
	def start_server(self, connections=15):
		self.SERVER.listen(connections)
		print("Waiting for connection...")
		
		CONNECTION_THREAD = Thread(target=self.accept_incoming_connections)
		CONNECTION_THREAD.daemon = True
		CONNECTION_THREAD.start()
		
	# Método de Finalização do Servidor
	def leave_server(self):
		print("Leaving the Server...")
		self.master.quit()
		self.SERVER.close()

	# Método de Envio de Comando para Atuadores via Socket
	def send_command(self,location,idx,command):
		actuator = self.tab2_frames[location][2][idx*2]
		actuator_text = self.tab2_frames[location][2][idx*2].get()
		
		parameters = self.tab2_frames[location][2][idx*2+1]
		parameters_text = self.tab2_frames[location][2][idx*2+1].get().split(" | ")

		for key,value in self.actuators_text.items():
			if(value[0] == location and value[1] == "_A:"+actuator_text):
				if(command == "power"):
					parameters_text[0] = "On" if (parameters_text[0] == "Off") else "Off"
				elif(command == "up" and len(parameters_text) > 1 and parameters_text[0] == "On"):
					parameters_text[1] = str(int(parameters_text[1])+1)
				elif(command == "down" and len(parameters_text) > 1 and parameters_text[0] == "On"):
					parameters_text[1] = str(int(parameters_text[1])-1)

				parameters_text = " | ".join(parameters_text)
				key.send(bytes(parameters_text, "utf8"))

				break

	# Método para Aceitar Conexões de Equipamentos (Clientes)
	def accept_incoming_connections(self):
		while True:
			client, client_address = self.SERVER.accept()
			print("%s:%s has connected." % client_address)
			
			client.send(bytes("Connected to the Gateway!", "utf8"))
			self.addresses[client] = client_address
			
			ACCEPT_THREAD = Thread(target=self.handle_client, args=(client,))
			ACCEPT_THREAD.daemon = True
			ACCEPT_THREAD.start()

	# Método (multithreaded) que administra as conexões com cada cliente
	def handle_client(self, client): 
		name, location = (client.recv(self.BUFSIZ).decode("utf8")).split("/")
		print(name, location)

		if(name[:3] == "_S:"): 
			textList = self.tab1_frames[location][2]
			textList[self.tab1_frames[location][1]].set(name[3:]+":")
			textList[self.tab1_frames[location][1]+1].set(0)

			self.sensors_text[client] = [location, name, self.tab1_frames[location][1]]

			self.tab1_frames[location][1] += 2

		elif(name[:3] == "_A:"):
			textList = self.tab2_frames[location][2]
			textList[self.tab2_frames[location][1]].set(name[3:])
			textList[self.tab2_frames[location][1]+1].set("Off")

			self.actuators_text[client] = [location, name, self.tab2_frames[location][1]]

			self.tab2_frames[location][1] += 2

		self.clients[client] = name
		client.send(bytes("OK", "utf8"))
		while True:
			msg = client.recv(self.BUFSIZ)
			if(name[:3] == "_S:"):
				textList = self.tab1_frames[location][2]
				idx = self.sensors_text[client][2]+1

				textList[idx].set(msg.decode("utf8"))

			elif(name[:3] == "_A:"):
				textList = self.tab2_frames[location][2]
				idx = self.actuators_text[client][2]+1

				textList[idx].set(msg.decode("utf8"))

# Loop Principal da Aplicação
if __name__ == "__main__":
	root = Tk()
	root.title("Dobotics Socket 1.0")
	root.geometry("800x600")
	root.resizable(0, 0)

	ServerApp(root)
	
	root.mainloop()
