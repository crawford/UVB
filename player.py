from logger import *
from board_objects import *
from game_board import *
from move import *

class Player(BoardObject):
	def __init__(self, username, connection):
		super(Player, self).__init__(0, 0)

		self.username = username
		self.connection = connection
		self.logger = create_logger(username)
		self.nextMove = (Act.STAY, Dir.N)

	def __str__(self):
		return '*'

	def disconnect(self):
		self.logger.info("Disconnecting")
		self.connection.close()

	def request_move(self, board):
		#nextMove = self.connection.get_move(board.getXML())
		self.nextMove = (Act.MOVE, Dir.S)

	def get_next_move(self):
		return self.nextMove

	def make_move(self, board):
		act,dir = self.nextMove
		x,y = board.nextPos(self.get_position(), dir)

		if act == Act.MOVE:
			board.moveObject(self, x, y)
			return
		elif act == Act.SNOWBALL:
			pass
		elif act == Act.SNOWMAN:
			board.addObject(SnowMan(), x, y)
			return
		else:
			return
			pass
