#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Thread
from time import sleep
from .ClientSocket import ClientSocket

class Actuator(ClientSocket):
	def __init__(self, name, location, var_init, bounds, serverIP, serverPort):
		ClientSocket.__init__(self, "_A:"+name+"/"+location, serverIP, serverPort)

		self.isOn = False
		self.act_var = var_init
		self.bounds = bounds

		self.actuator_name = "_A:"+name

		Thread(target=self.receive).start()

	def clipper(self):
		self.act_var = max(self.bounds[0], self.act_var)
		self.act_var = min(self.bounds[1], self.act_var)

	def receive(self):
		while True:
			try:
				msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")

				msg = msg.split(" | ")
				self.isOn = (msg[0].lower() == "on")

				if(len(msg) > 1):
					self.act_var = eval(msg[1])
					self.clipper()
					msg[1] = str(self.act_var)
				elif(self.act_var != None):
					msg.append(str(self.act_var))

				msg = " | ".join(msg)
				self.client_socket.send(bytes(msg, "utf8"))

			except OSError:  
				break