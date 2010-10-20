from constants import *
from player import *
from objects import *
from map import *
from math import sqrt

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

	def add_object(self, obj):
		self.add_object_to_board(obj)
		
		#add the object into the list
		if(isinstance(obj, Player)):
			self.players.append(obj)
		elif(isinstance(obj, DynamicObject)):
			self.dynamicObjects.append(obj)
		elif(isinstance(obj, StaticObject)):
			self.staticObjects.append(obj)

	# add an object to the game board
	def add_object_to_board(self, obj):
		#make sure the object is within the board
		if(not self.is_pos_on_board(obj.coordinates)):
			raise Exception("Object not within game board")

		#make sure there are no other object at the same location
		#if(self.get_object(obj.coordinates) != None):
		#	raise Exception("Already an object at that location");


		#if the rows are all empty, add the object at the first index
		if(len(self.rows) == 0):
			self.rows.insert(0, [obj])
			#self.printList()
			return

		for iRow in xrange(len(self.rows)):
			#if the new object is on the current row
			if(obj.get_y() == self.rows[iRow][0].get_y()):
				#check the x position of each object in the row
				for iCol in xrange(len(self.rows[iRow])):
					if(obj.get_x() < self.rows[iRow][iCol].get_x()):
						#if the new object is to the left of the current object, put it before it
						self.rows[iRow].insert(iCol, obj)
						#self.printList()
						return
					elif(obj.get_x() == self.rows[iRow][iCol].get_x()):
						raise NameError('Already an object at that position')

				#if the new object isn't left of any object, then its the farthest to the right
				self.rows[iRow].append(obj)
				#self.printList()
				return

			#if the new object is above than the current row
			if(obj.get_y() < self.rows[iRow][0].get_y()):
				#create a new row before the current one and add the object
				self.rows.insert(iRow, [obj])
				#self.printList()
				return

		#if the new object is below everything else add it to the bottom
		self.rows.append([obj])
		#self.printList()

	def printList(self):
		print 'List:'
		for row in self.rows:
			for obj in row:
				print obj.__str__(),
			print ''

	# remove an object from the game board
	def remove_object(self, obj):
		if(isinstance(obj, Player)):
			self.players.remove(obj)
		elif(isinstance(obj, DynamicObject)):
			self.dynamicObjects.remove(obj)
		elif(isinstance(obj, StaticObject)):
			self.staticObjects.remove(obj)

		self.remove_object_from_board(obj)

	def remove_object_from_board(self, obj):
		for row in self.rows:
			if(obj in row):
				row.remove(obj)
				if(len(row) == 0):
					self.rows.remove(row)
				break

	# move an object on the game board
	def move_object(self, obj, coordinates):
		if not self.is_pos_on_board(coordinates):
			return False

		self.remove_object_from_board(obj)
		obj.coordinates = coordinates
		self.add_object_to_board(obj)

		return True

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
		return (x < self.width and y < self.height and x >= 0 and y >= 0)

	def get_visible_board(self, (x, y), radius):
		map = GameMap()
		map.radius = radius

		# Loop through each row in the visible circle
		iRow = 0
		dy = y - radius
		while dy <= y + radius:
			# Find the desired row
			while iRow < len(self.rows) and self.rows[iRow][0].get_y() < dy:
				iRow += 1

			# Make sure we don't go beyond the end of the array
			if iRow == len(self.rows):
				break

			# Check to see if we skipped over it (the row we wanted was empty)
			if dy < self.rows[iRow][0].get_y():
				dy = self.rows[iRow][0].get_y()
				# make sure we haven't gone too far
				if dy > y + radius:
					continue


			# Calculate the valid width ( x^2 = r^2 - y^2 )
			ry = dy - y
			if ry == 0:
				row_width = radius
			else:
				row_width = sqrt(radius*radius - ry*ry)

			# Loop through the valid cols in the current row
			dx = x - row_width
			iCol = 0
			while dx <= x + row_width:
				# Find the desired col
				while iCol < len(self.rows[iRow]) and self.rows[iRow][iCol].get_x() < dx:
					iCol += 1

				# Make sure we don't go beyond the end of the array
				if iCol == len(self.rows[iRow]):
					break

				# Check to see if we skipped over it (no objects there)
				if dx < self.rows[iRow][iCol].get_x():
					dx = self.rows[iRow][iCol].get_x()
					# make sure we haven't gone too far
					if dx > x + row_width:
						continue

				# Add the object at this location
				map.objects[(dx - x, dy - y)] = str(self.rows[iRow][iCol])

				dx += 1

			dy += 1

		# Draw the edges (if any) on the map
		if not self.is_pos_on_board((x + radius, 0)):
			# Edge on the right side
			dx = self.width - x
			top_length = int(sqrt(radius*radius - dx*dx))
			bottom_length = top_length

			# Clip the edge so we don't draw too far
			if y - top_length < 0:
				top_length = y

			# Clip the edge so we don't draw too far
			if y + bottom_length > self.height:
				bottom_length = self.height - y

			for dy in xrange(-top_length, bottom_length + 1):
				map.objects[(dx, dy)] = map.EDGE

		if not self.is_pos_on_board((x - radius, 0)):
			# Edge on the left side
			dx = -x - 1
			top_length = int(sqrt(radius*radius - dx*dx))
			bottom_length = top_length

			# Clip the edge so we don't draw too far
			if y - top_length < 0:
				top_length = y + 1

			# Clip the edge so we don't draw too far
			if y + bottom_length > self.height:
				bottom_length = self.height - y

			for dy in xrange(-top_length, bottom_length + 1):
				map.objects[(dx, dy)] = map.EDGE

		if not self.is_pos_on_board((0, y + radius)):
			# Edge on the bottom side
			dy = self.height - y
			left_length = int(sqrt(radius*radius - dy*dy))
			right_length = left_length

			# Clip the edge so we don't draw too far
			if x - left_length < 0:
				left_length = x

			# Clip the edge so we don't draw too far
			if x + right_length > self.width:
				right_length = self.width - x

			for dx in xrange(-left_length, right_length + 1):
				map.objects[(dx, dy)] = map.EDGE

		if not self.is_pos_on_board((0, y - radius)):
			# Edge on the top side
			dy = -y - 1
			left_length = int(sqrt(radius*radius - dy*dy))
			right_length = left_length

			# Clip the edge so we don't draw too far
			if x - left_length < 0:
				left_length = x + 1

			# Clip the edge so we don't draw too far
			if x + right_length > self.width:
				right_length = self.width - x

			for dx in xrange(-left_length, right_length + 1):
				map.objects[(dx, dy)] = map.EDGE

	
		# Add the current player to the center of the map
		map.objects[(0, 0)] = map.ME

		return map

	def clear(self):
		pass
