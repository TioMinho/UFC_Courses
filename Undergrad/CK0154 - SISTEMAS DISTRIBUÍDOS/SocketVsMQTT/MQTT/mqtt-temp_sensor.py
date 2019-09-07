#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Bibliotecas
import paho.mqtt.client as paho
from random import random, uniform
import time

# Variáveis de Definição da Conexão
broker = "test.mosquitto.org"

# Conexão com o Broker
client= paho.Client("client-001")

print("Connecting to broker ", broker)
client.connect(broker)

# Início do Loop Principal
client.loop_start()

temperatura = 24
try:
    while True:
        if(random() < 0.2):
            # Simulação de Ruído no Sensor
            temperatura = temperatura + uniform(-0.001,0.001)   

            client.publish("house/temp_sensor", "{0:.2f} C".format(temperatura))
            time.sleep(2)

except KeyboardInterrupt:
    print("Exiting")
    client.disconnect
    client.loop_stop()
