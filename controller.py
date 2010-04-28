#!/usr/bin/python

from game_board import *
import ConfigParser

class Controller(object):
	def __init__(self):
		self.loadConfig("config")
		self.board = GameBoard(self.width, self.height)

	def loadConfig(self, filename):
		print "Loading game configuration..."
		config = ConfigParser.ConfigParser()
		config.read(filename)

		self.width = int(config.get("GameBoard", "Width"))
		self.height = int(config.get("GameBoard", "Height"))
		self.minvisibility = int(config.get("Player", "MinVisibility"))
		self.maxvisibility = int(config.get("Player", "MaxVisibility"))

		print " Min Visibility:", self.minvisibility
		print " Max Visibility:", self.maxvisibility
		print " Game Height:", self.height
		print " Game Width:", self.width




"""
		# get connections and wait for the start of the game
		self.get_players(datetime.timedelta(seconds=self.start_waittime))

		print "Starting game..."
		gamecount = 0

		# loop while the game hasn't run too long and there are still players
		while (gamecount < maxgamelength) and (len(self.players) > 1):
			# loop through all of the active players
				# create a derived gameboard for the specific player
				# send the gameboard to the player and ask for a move

			# apply all of the moves to the gameboard
				# if they moved, update their position on the map
				# if they made a snowball, increment their count
				# if they made a snowman, place a snowman on the map
				# if they threw a snowball, create a snowball in the direction on the map
			# check for any collisions between players and objects
				# if the player is in the same spot as another object, kill them
			pass
			#for p in self.players:
			#    p.join()
"""