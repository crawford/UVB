from objects import DynamicObject
import player

SPEED = 1

class Snowball(DynamicObject):
	owner = None
	direction = None
	speed = None

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
		global SPEED

		next_pos = self.coordinates

		for i in range(0, SPEED):
			next_pos = self.board.next_pos_in_direction(next_pos, self.direction, 1)
			
			if not self.board.is_pos_on_board(next_pos):
				self.kill()
				return

			if self.board.get_object(next_pos):
				break

		return next_pos

	def handle_collision(self, others):
		for obj in others:
			if(isinstance(obj, player.Player)):
				obj.increment_deaths()
				self.owner.increment_kills()
			else:
				pass
				
		self.kill()
