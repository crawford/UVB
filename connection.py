#!/usr/bin/python

import threading
import select

class Connection(threading.Thread):
	def __init__(self, socket):
		threading.Thread.__init__(self)
		self.socket = socket
		self.size = 1024
		self.timeout = 5

	def run(self):
		"""running = True
		while running:
			data = self.socket.recv(self.size)
			if data:
				self.socket.send(data)
			else:
				self.socket.close()
				running = False
		"""

		input = [self.socket]
		inready, outpready, exready = select.select(input, [], [], self.timeout)
		
		#if inready:
			#username = self.socket

	def close(self):
		self.socket.close()
