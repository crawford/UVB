from objects import DynamicObject
from player import *

class Snowball(DynamicObject):
	owner = None
	direction = None

	def __init__(self, board, coordinates, owner, direction):
		super(Snowball, self).__init__(board, coordinates)
		self.owner = owner
		self.direction = direction

	def __str__(self):
		return 'O';

	def serialize(self):
		old = super(Snowball, self).serialize()
		old['direction'] = self.direction
		return old

	def get_next_position(self):
		move = self.board.next_pos_in_direction((self.get_x(), self.get_y()), self.direction)
		if(self.board.is_pos_on_board(move)):
			return move
		else:
			self.kill()

	def handle_collision(self, others):
		print "entering collision"
		for obj in others:
			print "colliding with", obj
			if(isinstance(obj, Player)):
				#hurt the player
				pass
			else:
				print "killing"
				self.kill()
