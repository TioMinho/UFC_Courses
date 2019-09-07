#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Thread
from time import sleep
from .ClientSocket import ClientSocket

class SensorThread(Thread):
	def __init__(self, parent, delay):
		self.parent = parent
		self.delay = delay

		Thread.__init__(self)

	def run(self):
		while 1:
			self.parent.send()
			sleep(self.delay)

class Sensor(ClientSocket):
	def __init__(self, name, location, var_init, var_unit, bounds, serverIP, serverPort):
		ClientSocket.__init__(self, "_S:"+name+"/"+location, serverIP, serverPort)

		self.sensor_var = var_init
		self.var_unit = var_unit
		self.bounds = bounds

		self.sensorName = "_S:"+name
		self.sensorThread = SensorThread(self, 0.5)
		self.sensorThread.start()

	def clipper(self):
		self.sensor_var = max(self.bounds[0], self.sensor_var)
		self.sensor_var = min(self.bounds[1], self.sensor_var)

	def send(self): 
		"""Handles sending of messages."""
		msg = "{0:.2f} {1}".format(self.sensor_var, self.var_unit)
		self.client_socket.send(bytes(msg, "utf8"))