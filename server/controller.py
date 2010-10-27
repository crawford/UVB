from board import GameBoard
from tree import Tree
from player import Player
import snowball
from threading import Thread
from objects import DynamicObject
from objects import StaticObject
import logger
import ConfigParser
import time
import random

CONFIG_FILE = "config"

class Controller(object):
	logger = None
	board = None
	running = None
	paused = None
	width = None
	height = None
	minvisibility = None
	maxvisibility = None
	mintrees = None
	maxtrees = None
	visibility = None
	snapshot_file = None

	def __init__(self):
		self.logger = logger.create_logger('Controller')
		self.load_config(CONFIG_FILE)
		self.board = GameBoard(self.width, self.height)
		self.running = False
		self.paused = False
		self.visibility = random.randint(self.minvisibility, self.maxvisibility)
		
		# Put some trees on the board
		num_trees = random.randint(self.mintrees*self.width*self.height,
		                           self.maxtrees*self.width*self.height)

		for i in xrange(num_trees):
			x = random.randint(0, self.width - 1)
			y = random.randint(0, self.height - 1)

			if not self.board.get_object((x, y)):
				self.board.add_object(Tree(self.board, (x, y)))

	def load_config(self, filename):
		self.logger.info("Loading game configuration...")
		config = ConfigParser.ConfigParser()
		config.read(filename)

		self.snapshot_file = config.get("Server", "Snapshot")

		self.width = int(config.get("GameBoard", "Width"))
		self.height = int(config.get("GameBoard", "Height"))
		self.minvisibility = int(config.get("Player", "MinVisibility"))
		self.maxvisibility = int(config.get("Player", "MaxVisibility"))
		self.mintrees = float(config.get("GameBoard", "MinTrees"))
		self.maxtrees = float(config.get("GameBoard", "MaxTrees"))

		self.snowball_speed = int(config.get("Snowball", "Speed"))
		snowball.SPEED = self.snowball_speed

		self.logger.info("Min Visibility: " + str(self.minvisibility))
		self.logger.info("Max Visibility: " + str(self.maxvisibility))
		self.logger.info("Game Height: " + str(self.height))
		self.logger.info("Game Width: " + str(self.width))

	def create_player(self, username, connection):
		x = random.randint(0, self.width - 1)
		y = random.randint(0, self.height - 1)

		while self.board.get_object((x, y)):
			x = random.randint(0, self.width - 1)
			y = random.randint(0, self.height - 1)

		player = Player(username, connection, self.board, (x,y))
		return player

	def add_player(self, newPlayer):
		# check to see if player already exists
		if self.get_player(newPlayer.username):
			raise Exception('Player', 'Already exists')

		#add player to game
		self.board.add_object(newPlayer)

	def remove_player(self, player):
		self.board.remove_object(player)

	def get_player(self, name):
		for player in self.board.players:
			if player.username == name:
				return player

		return None

	def run(self):
		if(self.paused):
			self.logger.debug("Resuming game")
			self.paused = False
		else:
			self.logger.debug("Starting game")

		self.running = True
		snapshot_counter = 0

		while self.running and not self.paused and len(self.board.players) > 0 :
			self.step()
			time.sleep(1)
			
			snapshot_counter += 1
			if snapshot_counter == 10:
				snapshot_counter = 0
				file = open(self.snapshot_file, 'w')
				file.write(str(self.board))
				file.close()

		if self.running:
			self.logger.debug("Pausing game")
		else:
			# close the game
			self.logger.debug("Stopping game")
			#while len(self.board.players):
			#	self.board.players[0].disconnect()
			#	del self.board.players[0]

			self.board.clear()

		self.running = False

	def step(self):
		nextMoves = {}
		self.logger.debug("Getting players' moves")

		# for each player, create their visible map and ask for a move
		for player in self.board.players:
			if not player.connection.running:
				continue

			player.increment_steps()
			board = self.board.get_visible_board(player.coordinates, self.visibility)
			player.request_move(board)

		# wait for all of the players to respond (or timeout)
		for player in self.board.players:
			if player.connection.getting_move:
				player.connection.move_join()

			move = player.get_next_position()
			player.perform_action()
			#print move
			if move in nextMoves:
				nextMoves[move].append(player)
			else:
				nextMoves[move] = [player]

		# populate the nextMoves list with static objects
		for obj in self.board.staticObjects:
			if obj.coordinates in nextMoves:
				nextMoves[obj.coordinates].append(obj)
			else:
				nextMoves[obj.coordinates] = [obj]

		# populate the nextMoves list with dynamic objects
		for obj in self.board.dynamicObjects:
			move = obj.get_next_position()
			if move in nextMoves:
				nextMoves[move].append(obj)
			else:
				nextMoves[move] = [obj]


		# check for collisions and handle them
		for loc,lst in nextMoves.items():
			if len(lst) > 1:
				# if there are more than one object at that location
				for obj in lst:
					# loop through each of the objects and
					# have the dynamic ones handle the collision
					if(isinstance(obj, DynamicObject)):
						others = nextMoves[loc][:]
						others.remove(obj)
						obj.handle_collision(others)


		# apply all of the moves to the objects
		self.logger.debug("Applying moves")
		for obj in self.board.dynamicObjects:
			self.board.move_object(obj, obj.get_next_position())
		for player in self.board.players:
			if not self.board.move_object(player, player.get_next_position()):
				# if the player could not move (moved off game board)
				player.increment_deaths()

		#print self.board

	def pause(self):
		self.paused = True

	def resume(self):
		self.start()

	def stop(self):
		self.running = False

	def start(self):
		t = Thread(group = None, target = self.run)
		t.start()

	'''def reload_config(self):
		load_config(CONFIG_FILE)'''
