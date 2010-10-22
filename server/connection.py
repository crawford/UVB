from logger import *
from threading import Thread
from constants import Action, Direction
import db
import select
import sys
import ssl
import socket
import serialize

class Connection(object):
	socket = None
	hostname = None
	server = None
	size = None
	timeout = None
	logger = None
	running = None
	operation = None
	buffer = None
	readsize = None
	username = None
	move_thread = None
	next_move = None
	client_map = None

	def __init__(self, socket, hostname, server):
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
		self.username = ""
		self.move_thread = None
		self.next_move = (Action.NOP, Direction.NORTH)
		self.client_map = None

	def thrd_auth(self):
		#clear the buffer
		self.read_buffer()

		#request the key
		self.send_message('key')

		#if not self.peek_buffer():
		#wait for the response
		self.read_socket(self.readsize)

		secret = self.read_buffer()

		if not secret:
			self.logger.error("Response timed out from " + self.hostname)
			self.running = False
			return

		self.logger.debug("Received secret key from " + self.hostname + ": " + secret)

		self.username = db.get_username(secret)
		if not self.username:
			self.logger.error("Invalid key from " + self.hostname)
			self.send_message('0')
			self.running = False
			return

		self.logger.info(self.hostname + " authenticated as " + self.username)
		self.server.create_player(self.username, self)

		#Send positive confirmation
		self.send_message('1')

	def thrd_move(self):
		# Clear the buffer
		self.read_buffer()

		# Request the move
		self.send_message('move')
		
		# Send the map to the player
		self.send_message(serialize.dump(self.client_map))

		# Wait for the response
		self.read_socket(self.readsize)

		move = self.read_buffer()
		
		if not move:
			self.logger.error("Response timed out from " + self.username)
			return

		self.logger.info("Received move from " + self.username + ": " + move)

		act,dir = move.split(':')
		self.next_move = (int(act), int(dir))

	def send_message(self, message):
		try:
			self.socket.send(message)
		except:
			self.running = False

	def authenticate(self):
		t = Thread(group = None, target = self.thrd_auth)
		t.start()

	def get_move(self, map):
		self.client_map = map

		# Reset the move
		self.next_move = (Action.NOP, Direction.NORTH)
		
		# Wait for the response
		self.move_thread = Thread(group = None, target = self.thrd_move)
		self.move_thread.start()

	def move_join(self):
		self.move_thread.join()

	def is_running(self):
		#print "Checking"
		if self.running == False:
			return False
		
		#self.read_socket(self.readsize)
		return self.running

	def read_socket(self, length):
		#print "Attempting to read...",
		r, w, e = select.select([self.socket], [], [], self.timeout)
		if r:
			try:
				#print "Ready"
				data = self.socket.recv(length)
				#print "Read", data
				
				if data:
					self.buffer += data
				else:
					self.running = False
			except socket.error as error:
				self.logger.error(error)
				self.running = False
		else:
			#print "Not Ready"
			pass
			
	def read_buffer(self):
		out = self.buffer
		self.buffer = ""
		return out

	def peek_buffer(self):
		return self.buffer

	def close(self):
		self.running = False
		self.socket.close()
