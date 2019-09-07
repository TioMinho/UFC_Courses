#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from equips.Actuator import Actuator
from random import random, uniform
from time import sleep

actuators = []
actuators.append(Actuator("Lampada 1", "Sala", None, [], "127.0.0.1", 33000))
actuators.append(Actuator("Lampada 2", "Sala", None, [], "127.0.0.1", 33000))
actuators.append(Actuator("Lampada", "Cozinha", None, [], "127.0.0.1", 33000))
actuators.append(Actuator("Lampada", "Quarto", None, [], "127.0.0.1", 33000))
actuators.append(Actuator("Lampada", "Entrada", None, [], "127.0.0.1", 33000))
actuators.append(Actuator("Lampada", "Banheiro", None, [], "127.0.0.1", 33000))
actuators.append(Actuator("Ar-Condicionado", "Quarto", 24, [16,31], "127.0.0.1", 33000))
actuators.append(Actuator("Sprinklers", "Entrada", None, [], "127.0.0.1", 33000))
actuators.append(Actuator("Porta da Garagem", "Entrada", None, [], "127.0.0.1", 33000))
actuators.append(Actuator("Forno", "Cozinha", 30, [30, 100], "127.0.0.1", 33000))

try:
	while True:
		sleep(2)
		print("# SITUAÇÃO DOS ATUADORES #")
		print("Nome\t\t\t| Status\t| Parameter")
		for a in actuators:
			print("{0}:\t\t {1}\t| {2}".format(a.actuator_name, a.isOn, a.act_var))

except KeyboardInterrupt:
	print("Exiting...")
	for a in actuators:
		a.client_socket.close()