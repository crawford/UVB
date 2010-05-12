#!/usr/bin/python

from logger import *
import threading
import select
import sys
import ssl

class Connection(threading.Thread):
	def __init__(self, socket, hostname, server):
		threading.Thread.__init__(self)
		self.socket = socket
		self.hostname = hostname
		self.server = server
		self.size = 1024
		self.timeout = 10
		self.logger = create_logger(hostname)
		self.running = True

	def run(self):
		self.running = True
		self.socket.send('key')
		inready, outready, exready = select.select([self.socket], [], [], self.timeout)
	
		if not inready:
			self.logger.info("Response timed out")
			self.running = False
			return

		secret = self.socket.recv(40)
		self.logger.info("Received secret key: " + secret)

		# lookup secret key from redis
		# get username
		username = "testUser"

		self.logger.info("Authenticated as " + username)
		self.server.create_player(username, self)

	def close(self):
		self.socket.close()
