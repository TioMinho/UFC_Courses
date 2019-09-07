#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Bibliotecas
import paho.mqtt.client as paho
import time
from tkinter import *

# Variáveis Auxiliares
lampada_message = ''
arcond_message = ''
temp_sensor_message = ''
gelad_message = ''
porta_message = ''

# Definição das Função Auxiliares
def on_message(client, userdata, msg):
	global arcond_message, temp_sensor_message, gelad_message, porta_message
	
	if msg.topic == 'house/arcond':
		arcond_message = str(msg.payload.decode("utf8"))  
		print(msg.topic+"\t"+arcond_message)
	
	if msg.topic == 'house/temp_sensor':
		temp_sensor_message = str(msg.payload.decode("utf8"))
		print(msg.topic+"\t"+temp_sensor_message)
	
	if msg.topic == 'house/gelad':
		gelad_message = str(msg.payload.decode("utf8"))
		print(msg.topic+"\t"+gelad_message)
	
	if msg.topic == 'house/porta':
		porta_message  = str(msg.payload.decode("utf8"))
		print(msg.topic+"\t"+porta_message)

def update_value(state):
	global lampada_message
	lampada_message = state

# Definição das Classe Principal da Aplicação (Interface Gráfica)
class Application:
	# Construtor
	def __init__(self, master= None):
		# Atributos Auxiliares do Controlador
		self.lampada_message = ''
		self.arcond_message = ''
		self.temp_sensor_message = ''
		self.gelad_message = ''
		self.porta_message = ''
		
		# Atributos da Interface Gráfica
		self.fonte = ("Verdana", "8")
		
		self.container1 = Frame(master)
		self.container1["pady"] = 10
		self.container1.pack()
		
		self.lampada = Label(self.container1, text = "Lampada")
		self.lampada["font"] = ("Calibri", "10", "bold")
		self.lampada.grid(row=1, column=1, sticky=W, padx=5, pady=5)
		
		self.lamp_estado = Button(self.container1, text= 'OFF')
		self.lamp_estado["width"] = 10
		self.lamp_estado["font"] = self.fonte
		self.lamp_estado.bind("<Button-1>", self.mudarTexto)
		self.lamp_estado.grid(row=1, column=2, sticky=W, padx=5, pady=5)

		self.arcond = Label(self.container1, text = "Ar-Condicionado")
		self.arcond["font"] = ("Calibri", "10", "bold")
		self.arcond.grid(row=2, column=1, sticky=W, padx=5, pady=5)
		
		self.arcond_estado = Label(self.container1, text="On")
		self.arcond_estado["width"] = 10
		self.arcond_estado["font"] = self.fonte
		self.arcond_estado.grid(row=2, column=2, sticky=W, padx=5, pady=5)  
		
		self.temp_sensor = Label(self.container1, text = "Sensor de Temperatura")
		self.temp_sensor["font"] = ("Calibri", "10", "bold")
		self.temp_sensor.grid(row=3, column=1, sticky=W, padx=5, pady=5)
		
		self.temp_sensor_estado = Label(self.container1, text="On")
		self.temp_sensor_estado["width"] = 10
		self.temp_sensor_estado["font"] = self.fonte
		self.temp_sensor_estado.grid(row=3, column=2, sticky=W, padx=5, pady=5)  

		self.gelad = Label(self.container1, text = "Geladeira")
		self.gelad["font"] = ("Calibri", "10", "bold")
		self.gelad.grid(row=4, column=1, sticky=W, padx=5, pady=5)
		
		self.gelad_estado = Label(self.container1, text="On")
		self.gelad_estado["width"] = 10
		self.gelad_estado["font"] = self.fonte
		self.gelad_estado.grid(row=4, column=2, sticky=W, padx=5, pady=5) 
		
		self.porta = Label(self.container1, text = "Porta")
		self.porta["font"] = ("Calibri", "10", "bold")
		self.porta.grid(row=5, column=1, sticky=W, padx=5, pady=5)
		
		self.porta_estado = Label(self.container1, text="On")
		self.porta_estado["width"] = 10
		self.porta_estado["font"] = self.fonte
		self.porta_estado.grid(row=5, column=2, sticky=W, padx=5, pady=5)
		
	# Método para o Atuador
	def mudarTexto(self, event):
		if self.lamp_estado["text"] == "OFF":
			self.lamp_estado["text"] = "ON"
		else:
			self.lamp_estado["text"] = "OFF"

# Variáveis de Definição da Conexão
broker = "test.mosquitto.org"

# Definição do Cliente e Binding de Funções
client = paho.Client("Application1")

client.on_message = on_message

# Conexão com o Broker
print("Connecting to broker ", broker)
client.connect(broker)

# Início do Loop Principal
client.loop_start()
		
root = Tk()
root.title("Dobotics MQTT 1.0")
root.resizable(0, 0)

app = Application(master=root)

LOOP_ACTIVE =True
while LOOP_ACTIVE:
	root.update()
	client.subscribe([('house/arcond',2),('house/temp_sensor',2),('house/gelad',2),('house/porta',2)])
	
	app.temp_sensor_estado.configure(text=temp_sensor_message)
	app.arcond_estado.configure(text=arcond_message)
	app.gelad_estado.configure(text=gelad_message)
	app.porta_estado.configure(text=porta_message)
	
	client.publish("house/lampada", str(app.lamp_estado["text"]))
	client.loop(.1)
	
	time.sleep(.5)
	print(app.lamp_estado["text"])
