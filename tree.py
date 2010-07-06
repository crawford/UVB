from objects import StaticObject

class Tree(StaticObject):
	def __init__(self, board, coordinates):
		super(Tree, self).__init__(board, coordinates)

	def __str__(self):
		return "#"
