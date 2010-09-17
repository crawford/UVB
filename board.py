from constants import *
from player import *
from objects import *

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
				obj = self.get_object((x, y))
				if(obj == None):
					out += ' '
				else:
					out += obj.__str__()
			out += '|\n'
		out += '+' + '+'.rjust(self.width + 1, '-')
		return out

	# get object at (x,y) coordinate
	def get_object(self, (x, y)):
		#TODO: more efficient
		for row in self.rows:
			for obj in row:
				if(obj.get_x() == x and obj.get_y() == y):
					return obj
		return None

	# add an object to the game board
	def add_object(self, obj):
		#make sure the object is within the board
		if(not self.is_pos_on_board(obj.coordinates)):
			raise Exception("Object not within game board")

		#make sure there are no other object at the same location
		#if(self.get_object(obj.coordinates) != None):
		#	raise Exception("Already an object at that location");

		#add the object into the list
		if(isinstance(obj, Player)):
			self.players.append(obj)
		elif(isinstance(obj, DynamicObject)):
			self.dynamicObjects.append(obj)
		elif(isinstance(obj, StaticObject)):
			self.staticObjects.append(obj)

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
		for row in self.rows:
			if(obj in row):
				row.remove(obj)
				if(len(row) == 0):
					self.rows.remove(row)
				break

		if(isinstance(obj, Player)):
			self.players.remove(obj)
		elif(isinstance(obj, DynamicObject)):
			self.dynamicObjects.remove(obj)
		elif(isinstance(obj, StaticObject)):
			self.staticObjects.remove(obj)

	# move an object on the game board
	def move_object(self, obj, coordinates):
		self.remove_object(obj)
		obj.coordinates = coordinates
		self.add_object(obj)

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

	def is_pos_on_board(self, (x, y)):
		return (x < self.width or y < self.height or x >= 0 or y >= 0)

	def get_visible_board(self, (x, y), radius):
		pass

	def clear(self):
		pass