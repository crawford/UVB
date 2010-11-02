from constants import Action
from constants import Direction

class GameObject(object):
	board = None
	coordinates = None
	killed = None

	def __init__(self, board, coordinates):
		self.board = board
		self.coordinates = coordinates
		self.killed = False

	def serialize(self):
		return {'type': self.__class__.__name__, 'coordinates':self.coordinates}

	def get_x(self):
		return self.coordinates[0]

	def get_y(self):
		return self.coordinates[1]

	def kill(self):
		if not self.killed:
			self.killed = True
			self.board.remove_object(self)


class DynamicObject(GameObject):
	def __init__(self, board, coordinates):
		super(DynamicObject, self).__init__(board, coordinates)

	def get_next_position(self, next_moves):
		pass

	def handle_collision(self, others):
		pass

	def serialize(self):
		return super(DynamicObject, self).serialize()


class StaticObject(GameObject):
	pass
