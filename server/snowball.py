from objects import DynamicObject
import player

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
		move = self.board.next_pos_in_direction((self.get_x(), self.get_y()), self.direction, 2)

		if(self.board.is_pos_on_board(move)):
			return move
		else:
			self.kill()

	def handle_collision(self, others):
		for obj in others:
			if(isinstance(obj, player.Player)):
				obj.increment_deaths()
				self.owner.increment_kills()
			else:
				pass
				
		self.kill()
