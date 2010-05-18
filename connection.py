#!/usr/bin/python

from logger import *
import db
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
		self.readsize = 1024

	def run(self):
		if self.operation == AUTH:
			self.socket.send('key')

			if not self.peek_buffer():
				r, w, e = select.select([self.socket], [], [], self.timeout)
				self.read_socket(self.readsize)

			secret = self.read_buffer()
		
			if not secret:
				self.logger.info("Response timed out from " + self.hostname)
				self.running = False
				return

			self.logger.debug("Received secret key from " + self.hostname + ": " + secret)
			
			username = db.get_username(secret)
			if not username:
				self.logger.info("Invalid key from " + self.hostname)
				self.running = False
				return

			self.logger.info(self.hostname + " authenticated as " + username)
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
		
		self.read_socket(self.readsize)
		return self.running

	def read_socket(self, length):
		print "Attempting to read...",
		r, w, e = select.select([self.socket], [], [], 0)
		if r:
			try:
				print "Ready"
				data = self.socket.recv(length)
				print "Read", data
				
				if data:
					self.buffer += data
				else:
					self.running = False
			except socket.error as error:
				print error
				self.running = False
		else:
			print "Not Ready"
			
	def read_buffer(self):
		out = self.buffer
		self.buffer = ""
		return out

	def peek_buffer(self):
		return self.buffer

	def close(self):
		self.running = False
		self.socket.close()
