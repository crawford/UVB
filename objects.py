from constants import *

class GameObject(object):
	board = None
	coordinates = None

	def __init__(self, board, coordinates):
		self.board = board
		self.coordinates = coordinates

	def serialize(self):
		return {'type': self.__class__.__name__, 'coordinates':self.coordinates}

	def get_x(self):
		return self.coordinates[0]

	def get_y(self):
		return self.coordinates[1]


class DynamicObject(GameObject):
	def __init__(self, board, coordinates):
		super(DynamicObject, self).__init__(board, coordinates)

	def getNextPosition(self):
		pass

	def handleCollision(self):
		pass

	def serialize(self):
		return super(DynamicObject, self).serialize()


class StaticObject(GameObject):
	pass