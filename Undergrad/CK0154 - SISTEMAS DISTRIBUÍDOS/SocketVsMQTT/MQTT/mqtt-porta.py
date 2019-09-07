#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Bibliotecas
import paho.mqtt.client as paho
import time

# Variáveis de Definição da Conexão
broker = "test.mosquitto.org"

# Conexão com o Broker
client= paho.Client("client-004")

print("Connecting to broker ", broker)
client.connect(broker)

# Início do Loop Principal
client.loop_start()
try:
	while True:
		client.publish("house/porta", str("Trancada"))
		time.sleep(2)

except KeyboardInterrupt:
	print("Exiting")
	client.disconnect
	client.loop_stop()
