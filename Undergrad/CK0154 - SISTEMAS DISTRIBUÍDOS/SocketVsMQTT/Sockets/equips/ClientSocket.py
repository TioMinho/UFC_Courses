#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM

class ClientSocket(object):
	def __init__(self, name, serverIP, serverPort):
		self.name = name
		self.serverIP = serverIP
		self.serverPort = serverPort

		self.BUFSIZ = 1024
		self.ADDR = (self.serverIP, self.serverPort)

		self.client_socket = socket(AF_INET, SOCK_STREAM)
		self.handshake()

	def handshake(self):
		self.client_socket.connect(self.ADDR)

		try:
			msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")
		except OSError: 
			print("Error")

		self.client_socket.send(bytes(self.name, "utf8"))
		self.client_socket.recv(self.BUFSIZ).decode("utf8")
		print(self.name + " CONNECTED")

	def receive(self):
		"""Handles receiving of messages."""
		return None

	def send(self): 
		"""Handles sending of messages."""
		return None