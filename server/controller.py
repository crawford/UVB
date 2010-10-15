from logger import *
from board import *
import ConfigParser
from threading import Thread
import time

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

	def __init__(self):
		self.logger = create_logger('Controller')
		self.load_config(CONFIG_FILE)
		self.board = GameBoard(self.width, self.height)
		self.running = False
		self.paused = False

	def load_config(self, filename):
		self.logger.info("Loading game configuration...")
		config = ConfigParser.ConfigParser()
		config.read(filename)

		self.width = int(config.get("GameBoard", "Width"))
		self.height = int(config.get("GameBoard", "Height"))
		self.minvisibility = int(config.get("Player", "MinVisibility"))
		self.maxvisibility = int(config.get("Player", "MaxVisibility"))

		self.logger.info("Min Visibility: " + str(self.minvisibility))
		self.logger.info("Max Visibility: " + str(self.maxvisibility))
		self.logger.info("Game Height: " + str(self.height))
		self.logger.info("Game Width: " + str(self.width))

	def create_player(self, username, connection):
		player = Player(username, connection, self.board, (0,0))
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

		#while self.running and not self.paused and len(self.board.players):
		while self.running and not self.paused:
			self.step()
			time.sleep(1)

		if self.running:
			self.logger.debug("Pausing game")
		else:
			# close the game
			self.logger.debug("Stopping game")
			while len(self.board.players):
				self.board.players[0].disconnect()
				del self.board.players[0]

			self.board.clear()

	def step(self):
		nextMoves = {}
		self.logger.debug("Step")

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

		self.logger.debug("Getting players' moves")

		# for each player, create their visible map and ask for a move
		for player in self.board.players:
			board = self.board.getVisibleBoard((player.get_x(), player.get_y()), self.maxvisibility)
			player.request_move(board)

		# wait for all of the players to respond (or timeout)
		for player in self.board.players:
			player.connection.join()
			move = player.get_next_position()
			if move in nextMoves:
				nextMoves[move].append(player)
			else:
				nextMoves[move] = [player]

		print nextMoves

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
			self.board.move_object(player, player.get_next_position())

		print self.board

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
