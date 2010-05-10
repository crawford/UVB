#!/usr/bin/python

from logger import *
import threading
import select
import sys
import ssl

class Connection(threading.Thread):
	def __init__(self, socket, hostname):
		threading.Thread.__init__(self)
		self.socket = socket
		self.hostname = hostname
		self.size = 1024
		self.timeout = 10
		self.logger = createLogger(hostname)

	def run(self):
		self.socket.send('key')
		inready, outready, exready = select.select([self.socket], [], [], self.timeout)
	
		if inready:
			secret = self.socket.recv(40)
			self.logger.info("Received secret key: " + secret)
			
		self.logger.info("Going idle")

	def close(self):
		self.socket.close()
