#!/usr/bin/python

from logger import *
from game_board import *
import ConfigParser
import threading

CONFIG_FILE = "config"

class Controller(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

		self.logger = create_logger('Controller')
		self.load_config(CONFIG_FILE)
		self.board = GameBoard(self.width, self.height)
		self.running = True
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

	def add_player(self, newPlayer):
		# check to see if player already exists
		if self.get_player(newPlayer.username):
			raise Exception('Player', 'Already exists')
			return

		#add player to game
		self.board.addObject(newPlayer)

	def get_player(self, name):
		for player in self.board.players:
			if player.username == name:
				return player

		return None

	def run(self):
		self.logger.debug("Starting/Resuming game")

		while self.running and not self.paused and len(self.board.players):
			self.step()

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

		# populate the nextMoves list with static objects
		


		# for each player, create their visible map and ask for a move
		self.logger.debug("Step")
		for player in self.board.players:
			board = self.board.getVisibleBoard(player.x, player.y, self.maxvisibility)
			player.request_move(board)

		# wait for all of the players to respond (or timeout)
		self.logger.debug("Getting players' moves")
		for player in self.board.players:
			player.connection.join()
			move = player.get_next_move()
			try:
				nextMoves[move].append(player)
			except KeyError:
				nextMoves[move] = [player]

		# apply all of the moves to the snowballs
		for ball in self.board.snowballs:
			move = ball.get_next_move()
			try:
				nextMoves[move].append(ball)
			except KeyError:
				nextMoves[move] = list(ball)

		# check for collisions and handle them
		for loc,lst in nextMoves.items():
			if len(lst) > 1:
				# if there are more than one object at that location
				for obj in lst:
					# loop through each of the objects
					# and have them handle the collision
					others = loc
					others.remove(obj)
					obj.handle_collision(others)

		
		# apply all of the moves to the objects
		self.logger.debug("Applying moves")
		for player in self.board.players:
			player.make_move(self.board)
		for snowball in self.board.snowballs:
			snowball.make_move(self.board)

		print self.board

	def pause(self):
		self.paused = True

	def resume(self):
		self.paused = False
		self.start()

	def stop(self):
		self.running = False

	'''def reload_config(self):
		load_config(CONFIG_FILE)'''
