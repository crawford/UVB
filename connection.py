#!/usr/bin/python

from logger import *
import threading
import select
import sys
import ssl
import socket

AUTH, GET_MOVE = range(2)

class Connection(threading.Thread):
	def __init__(self, socket, hostname, server):
		threading.Thread.__init__(self)

		self.socket = socket
		self.hostname = hostname
		self.server = server
		self.size = 1024
		self.timeout = 10
		self.logger = server.logger
		self.running = True
		self.operation = None
		self.buffer = ""

	def run(self):
		if self.operation == AUTH:
			self.socket.send('key')
			inready, outready, exready = select.select([self.socket], [], [], self.timeout)
			self.read_socket(40)
			secret = self.read_buffer()
		
			if not secret:
				self.logger.info("Response timed out from " + self.hostname)
				self.running = False
				return

			self.logger.info("Received secret key from " + self.hostname + ": " + secret)
			# lookup secret key from redis
			# get username
			username = "testUser"

			self.logger.info(self.hostname + " authenticated as " + username)
			self.logger = create_logger(username)
			self.server.create_player(username, self)
		elif self.operation == GET_MOVE:
			pass

	def authenticate(self):
		self.operation = AUTH
		self.start()

	def is_running(self):
		print "Checking"
		if self.running == False:
			return False

		try:
			self.read_socket(1)
		except Exception as e:
			print e
			return False
		return True

	def read_socket(self, length):
		r,w,e = select.select([self.socket], [], [], 0)
		if r:
			data = self.socket.recv(length)
			if data:
				self.buffer += data
			else:
				raise Exception('Socket', 'Disconnected')
			
	def read_buffer(self):
		out = self.buffer
		self.buffer = ""
		return out

	def close(self):
		self.socket.close()
