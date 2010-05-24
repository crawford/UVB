from logger import *
from board_objects import *
from game_board import *

class Player(BoardObject):
	def __init__(self, username, connection):
		super(BoardObject, self).__init__()

		self.username = username
		self.connection = connection
		self.logger = create_logger(username)
		self.next_move = (STAY, N)

	def __str__(self):
		return '*'

	def disconnect(self):
		self.logger.info("Disconnecting")
		self.connection.close()

	def request_move(self, board):
		self.connection.get_move(board.getXML())

	def make_move(self, board):
		act,dir = self.next_move
		x,y = board.nextPos(self.getPosition())

		if act == MOVE:
			obj = board.get_at(x, y)
			if obj == None:
				board.moveObject(self, x, y)
				return
			elif type(obj) is SnowBall or type(obj) is SnowMan:
				board.removeObject(obj)
				board.moveObject(self, x, y)
				self.hit()
			elif type(obj) is Tree:
				self.hit()
		elif act == SNOWBALL:
			pass
		elif act == SNOWMAN:
			pass
		else:
			pass
