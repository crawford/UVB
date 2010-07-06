from objects import DynamicObject

class Snowball(DynamicObject):
	owner = None
	direction = None

	def __init__(self, board, coordinates, owner, direction):
		super(Snowball, self).__init__(board, coordinates)
		self.owner = owner
		self.direction = direction

	def serialize(self):
		old = super(Snowball, self).serialize()
		old['direction'] = self.direction
		return old

	def __str__(self):
		return 'O';
