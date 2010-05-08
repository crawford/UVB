#!/usr/bin/python

import threading
import select
import sys

class Connection(threading.Thread):
	def __init__(self, socket):
		threading.Thread.__init__(self)
		self.socket = socket
		self.size = 1024
		self.timeout = 10

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
	
		self.socket.send('key')

		'''inready, outready, exready = select.select([self.socket], [], [self.socket], self.timeout)
	
		print 'a'
		if inready:
			print 'b'
			username = self.socket.recv(1024)
			print username
		if outready:
			print 'c'
		if exready:
			print 'd'
			'''



	def close(self):
		self.socket.close()
