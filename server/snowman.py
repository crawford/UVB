from objects import StaticObject

class Snowman(StaticObject):
	owner = None

	def __init__(self, board, coordinates, owner):
		super(Snowman, self).__init__(board, coordinates)
		self.owner = owner

	def __str__(self):
		return "8"
