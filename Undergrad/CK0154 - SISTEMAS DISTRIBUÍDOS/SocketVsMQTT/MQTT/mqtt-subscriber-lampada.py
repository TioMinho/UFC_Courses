#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Bibliotecas
import paho.mqtt.client as paho
import time

# Variáveis de Definição da Conexão
broker = "test.mosquitto.org"

# Definição das Função de Atuação
def on_message(client, userdata, message):
	time.sleep(.5)
	print("Received message: ", str(message.payload.decode("utf-8")))

# Definição do Cliente e Binding de Funções
client= paho.Client("client-005")

client.on_message = on_message

# Conexão com o Broker
print("Connecting to broker ", broker)
client.connect(broker)

# Início do Loop Principal
client.loop_start()

print("Subscribing the Actuator")
client.subscribe("house/lampada") 

try:
	while True:
		time.sleep(.1)

except KeyboardInterrupt:
	print("Exiting")
	client.disconnect
	client.loop_stop()
