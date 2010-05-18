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

	def add_player(self, newPlayer):
		# check to see if player already exists
		if self.get_player(newPlayer.username):
			raise Exception('Player', 'Already exists')
			return

		#add player to game
		self.board.players.append(newPlayer)

	def get_player(self, name):
		for player in self.board.players:
			if player.username == name:
				return player

		return None

	def run(self):
		self.logger.debug("Starting/Resuming game")
		self.running = True
		self.paused = False

		while self.running and not self.paused and len(self.players):
			self.logger.debug("Step")
			# for each player, create their visible map and ask for a move
			for player in self.board.players:
				board = self.board.getVisibleBoard(player.x, player.y, self.maxvisibility)
				player.request_move(board)

			# wait for all of the players to respond (or timeout)
			for player in self.board.players:
				player.join()

			self.logger.debug("Moving snowballs")
			# apply all of the moves to the snowballs
			for ball in self.board.snowballs:
				ball.make_move()

			self.logger.debug("Moving players")
			# apply all of the moves to the players
			for player in self.board.players:
				player.make_move(self.board)

		if self.running:
			self.logger.debug("Pausing game")
		else:
			# close the game
			self.logger.debug("Stopping game")
			while len(self.board.players):
				player.disconnect()
				del player

			self.board.clear()

	def pause(self):
		self.paused = True

	def resume(self):
		self.start()

	def stop(self):
		self.running = False

	def reload_config(self):
		load_config(CONFIG_FILE)
