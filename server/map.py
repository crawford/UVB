from constants import Direction


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
		out = '+' + '+'.rjust(self.radius*4 + 4, '-') + '\n'
		for y in range(-self.radius, self.radius + 1):
			out += '| '
			for x in range(-self.radius, self.radius + 1):
				if str((x, y)) in self.objects:
					out += self.objects[str((x, y))]
				else:
					out += ' '

				out += ' '
			out += '|\n'
		out += '+' + '+'.rjust(self.radius*4 + 4, '-')

		return out

	def get_object_at(self, coordinates):
		if str(coordinates) in self.objects:
			return self.objects[str(coordinates)]
		else:
			return None

	def next_pos_in_direction(self, (x, y), direction):
		if direction == Direction.NORTH:
			y -= 1
		elif direction == Direction.NORTHEAST:
			y -= 1
			x += 1
		elif direction == Direction.EAST:
			x += 1
		elif direction == Direction.SOUTHEAST:
			y += 1
			x += 1
		elif direction == Direction.SOUTH:
			y += 1
		elif direction == Direction.SOUTHWEST:
			y += 1
			x -= 1
		elif direction == Direction.WEST:
			x -= 1
		elif direction == Direction.NORTHWEST:
			y -= 1
			x -= 1
		return (x, y)

	def rotate_left(self, current):
		return (int(current) + 7) % 8

	def rotate_right(self, current):
		return (int(current) + 1) % 8
