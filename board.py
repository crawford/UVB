from constants import *

class GameBoard(object):
	width = None
	height = None
	dynamicObjects = None
	staticObjects = None
	players = None
	board = None

	def __init__(self, width, height, players = None):
		self.width = width
		self.height = height
		self.dynamicObjects = []
		self.staticObjects = []
		self.players = []
		self.rows = []

	# convert the game board to a string
	def __str__(self):
		#TODO: could be more efficient, probably will be removed
		out = '+' + '+'.rjust(self.width + 1, '-') + '\n'
		for y in xrange(self.height):
			out += '|'
			for x in xrange(self.width):
				obj = self.get_object(x, y)
				if(obj == None):
					out += ' '
				else:
					out += obj.__str__()
			out += '|\n'
		out += '+' + '+'.rjust(self.width + 1, '-')
		return out

	# get object at (x,y) coordinate
	def get_object(self, x, y):
		#TODO: more efficient
		for row in self.rows:
			for obj in row:
				if(obj.get_x() == x and obj.get_y() == y):
					return obj
		return None

	# add an object to the game board
	def add_object(self, obj):
		#if the rows are all empty, add the object at the first index
		if(len(self.rows) == 0):
			self.rows.insert(0, [obj])
			self.printList()
			return

		for iRow in xrange(len(self.rows)):
			#if the new object is on the current row
			if(obj.get_y() == self.rows[iRow][0].get_y()):
				#check the x position of each object in the row
				for iCol in xrange(len(self.rows[iRow])):
					if(obj.get_x() < self.rows[iRow][iCol].get_x()):
						#if the new object is to the left of the current object, put it before it
						self.rows[iRow].insert(iCol, obj)
						self.printList()
						return
					elif(obj.get_x() == self.rows[iRow][iCol].get_x()):
						raise NameError('Already an object at that position')

				#if the new object isn't left of any object, then its the farthest to the right
				self.rows[iRow].append(obj)
				self.printList()
				return

			#if the new object is above than the current row
			if(obj.get_y() < self.rows[iRow][0].get_y()):
				#create a new row before the current one and add the object
				self.rows.insert(iRow, [obj])
				self.printList()
				return

		#if the new object is below everything else add it to the bottom
		self.rows.append([obj])
		self.printList()

	def printList(self):
		print 'List:'
		for row in self.rows:
			for obj in row:
				print obj.__str__(),
			print ''

	# remove an object from the game board
	def remove_object(self, obj):
		pass

	# move an object on the game board
	def move_object(self, obj, x, y):
		pass

	def next_pos(self, (x, y), direction):
		if direction == Direction.N:
			y += 1
		elif direction == Direction.NE:
			y += 1
			x += 1
		elif direction == Direction.E:
			x += 1
		elif direction == Direction.SE:
			y -= 1
			x += 1
		elif direction == Direction.S:
			y -= 1
		elif direction == Direction.SW:
			y -= 1
			x -= 1
		elif direction == Direction.W:
			x -= 1
		elif direction == Direction.NW:
			y += 1
			x -= 1
		return (x, y)

	def get_visible_board(self,x,y,radius):
		pass

	def clear(self):
		pass