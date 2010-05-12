from logger import *

class Player(object):
	def __init__(self, username, connection):
		self.username = username
		self.connection = connection
		self.logger = create_logger(username)
