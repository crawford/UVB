from objects import DynamicObject
from constants import Direction
from constants import Action
from snowball import Snowball
from tree import Tree
import logger
import db
import time

class Player(DynamicObject):
	username = None
	connection = None
	logger = None

	def __init__(self, username, connection, board, position):
		super(Player, self).__init__(board, position)

		self.username = username
		self.connection = connection
		self.logger = logger.create_logger(username)

	def __str__(self):
		return '*'

	def disconnect(self):
		self.logger.info("Disconnecting")
		self.connection.close()

	def increment_kills(self):
		self.logger.debug(self.username + " hit another player")
		db.increment_kills(self.username)

	def increment_steps(self):
		db.increment_steps(self.username)

	def increment_deaths(self):
		self.logger.debug(self.username + " died")
		db.increment_deaths(self.username)

	def request_move(self, board):
		self.connection.get_move(board)

	def get_next_position(self):
		if self.connection.next_move[0] == Action.MOVE:
			return self.board.next_pos_in_direction(self.coordinates,
                                                    self.connection.next_move[1])

		return self.coordinates

	def perform_action(self):
		if self.connection.next_move[0] == Action.THROWSNOWBALL:
			self.board.add_object(Snowball(self.board,
			                               self.coordinates,
										   self,
										   self.connection.next_move[1]))

	def handle_collision(self, others):
		for obj in others:
			if (isinstance(obj, Snowball)):
				obj.owner.increment_kills()
				self.increment_deaths()

			if (isinstance(obj, Player)):
				obj.increment_deaths()
				self.increment_kills()

			if (isinstance(obj, Tree)):
				self.connection.next_move = (Action.NOP, Direction.NORTH)
				self.increment_deaths()

