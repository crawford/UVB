from logger import *
from objects import *
from constants import *
from snowball import *
import time

class Player(DynamicObject):
	username = None
	connection = None
	logger = None

	def __init__(self, username, connection, board, position):
		super(Player, self).__init__(board, position)

		self.username = username
		self.connection = connection
		self.logger = create_logger(username)

	def __str__(self):
		return '*'

	def disconnect(self):
		self.logger.info("Disconnecting")
		self.connection.close()

	def increment_kills(self, player):
		logger.debug(self.username + " hit " + player.username)
		#TODO: update db

	def increment_steps(self):
		pass
		#TODO: update db

	def increment_deaths(self):
		logger.debug(self.username + " died")
		#TODO: update db

	def request_move(self, board):
		self.connection.get_move(board)

	def get_next_position(self):
		if self.connection.next_move[0] == Action.MOVE:
			return self.board.next_pos_in_direction(self.coordinates,
                                                    self.connection.next_move[1])

		return self.coordinates

	def handle_collision(self, others):
		for obj in others:
			if(isinstance(obj, Snowball)):
				obj.owner.increment_kills(self)
				self.increment_deaths()
