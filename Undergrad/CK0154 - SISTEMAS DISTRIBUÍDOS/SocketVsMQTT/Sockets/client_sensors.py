#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from equips.Sensor import Sensor
from random import random, uniform
from time import sleep

sensors = []
sensors.append(Sensor("Temperatura", "Sala", 24.0, "C", [-99,99], "127.0.0.1", 33000))
sensors.append(Sensor("Temperatura", "Sala", 24.0, "C", [-99,99], "127.0.0.1", 33000))
sensors.append(Sensor("Temperatura", "Cozinha", 24.0, "C", [-99,99], "127.0.0.1", 33000))
sensors.append(Sensor("Água", "Cozinha", 20, "L", [0,20], "127.0.0.1", 33000))
sensors.append(Sensor("Gás", "Cozinha", 0, "ppm", [0,100], "127.0.0.1", 33000))
sensors.append(Sensor("Temperatura", "Quarto", 24.0, "C", [-99,99], "127.0.0.1", 33000))
sensors.append(Sensor("Temperatura", "Entrada", 24.0, "C", [-99,99], "127.0.0.1", 33000))
sensors.append(Sensor("Presença", "Entrada", 0, "", [0,1], "127.0.0.1", 33000))
sensors.append(Sensor("Temperatura", "Banheiro", 24.0, "C", [-99,99], "127.0.0.1", 33000))

try:
	while True:
		sleep(.5)
		for s in sensors:
			if(random() < 0.5):
				s.sensor_var = s.sensor_var+uniform(-0.01,0.01)
				s.clipper()

except KeyboardInterrupt:
	print("Exiting...")
	for s in sensors:
		S.client_socket.close()