#!/usr/bin/python

class Connection(threading.Thread):
	def __init__(self, (socket, address), server):
		threading.Thread.__init__(self)
		self.socket = socket
		self.address = address
		self.server = server
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
