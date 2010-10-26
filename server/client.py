#!/usr/bin/python

from threading import Thread
import socket
import select
import ssl
import serialize


class Client(Thread):
	SERVER = None
	PORT = None
	KEY = None
	sock = None
	connected = None
	decide_move = None
	running = None


	def __init__(self):
		Thread.__init__(self)
		self.SERVER = 'uvb.csh.rit.edu'
		self.PORT = 13783
		self.KEY = ''
		self.sock = None
		self.connected = False
		self.decide_move = None
		self.running = False



	def connect(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.settimeout(5)
		self.sock = ssl.wrap_socket(self.sock, ca_certs="opcomm.crt", cert_reqs=ssl.CERT_REQUIRED)
		self.sock.connect((self.SERVER, self.PORT))

		inready, outready, exready = select.select([self.sock], [], [], 5)

		if inready:
			# clear the buffer (should be 'key')
			response = self.sock.recv(100)
		else:
			self.connected = False
			return False

		inready, outready, exready = select.select([], [self.sock], [], 5)

		if outready:
			self.sock.send(self.KEY)

		inready, outready, exready = select.select([self.sock], [], [], 5)

		if inready:
			response = self.sock.recv(1)
			if response == '1':
				self.connected = True
				return True
			
		self.connected = False
		return False



	def run(self):
		if not self.connected:
			return

		self.running = True

		while self.running:
			inready, outready, exready = select.select([self.sock], [], [], 5)

			if inready:
				response = self.sock.recv(4)

				# Check for a closed connection
				if response == '':
					return

				if response != 'move':
					continue

				response = self.sock.recv(10000)
				board = serialize.load(response)
				move = self.decide_move(board)
				self.send_move(move[0], move[1])



	def send_move(self, act, dir):
		# Clear the buffer
		#self.sock.recv(100)

		'''while True:
			inready, outready, exready = select.select([self.sock], [], [], 5)
			if inready:
				response = self.sock.recv(4)
				if response == 'move':
					break;
				print response'''


		self.sock.send(str(act) + ':' + str(dir))



	def stop(self):
		self.running = False



	def disconnect(self):
		self.sock.close()
		self.connected = False

