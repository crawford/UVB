from logger import *

class Player(object):
	def __init__(self, username, connection):
		self.username = username
		self.connection = connection
		self.logger = create_logger(username)

	def disconnect(self):
		self.logger.info("Disconnecting")
		self.connection.close()

	def request_move(self):
		pass

	def get_move(self):
		pass
