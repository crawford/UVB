

class GameMap(object):
	objects = None
	radius = None
	TREE = None
	PLAYER = None
	SNOWBALL = None
	SNOWMAN = None
	EDGE = None

	def __init__(self):
		self.objects = {}
		self.radius = 0
		self.TREE = '^'
		self.PLAYER = '*'
		self.SNOWBALL = 'O'
		self.SNOWMAN = '8'
		self.EDGE = '#'
		self.ME = 'X'
		self.UNKNOWN = '?'

	def __str__(self):
		out = '+' + '+'.rjust(self.radius*2 + 2, '-') + '\n'
		for y in range(-self.radius, self.radius + 1):
			out += '|'
			for x in range(-self.radius, self.radius + 1):
				if str((x, y)) in self.objects:
					out += self.objects[str((x, y))]
				else:
					out += ' '
			out += '|\n'
		out += '+' + '+'.rjust(self.radius*2 + 2, '-')

		return out

	def get_object_at(self, coordinates):
		if coordinates in self.objects:
			return self.objects[coordinates]
		else:
			return None
