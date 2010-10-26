#!/usr/bin/python

from client import Client
from constants import Action, Direction
import random

# This function is called everytime the client gets a new map.
# It decides what move to make and returns the decision.
# The client module takes care of the network communication magic.
def dummy(board):
	# We need this variable to keep state between moves
	global last_dir

	# Print out our view of the game board
	print board

	# Pre-load 'obj' with a non-None value (python doesn't have do-while loops)
	obj = 1

	# Keep trying a random direction until there is no object in our way
	while obj:
		# Get the next cell in our current path (last_dir)
		next_pos = board.next_pos_in_direction((0, 0), last_dir)

		# Get the object at that next cell
		obj = board.get_object_at(next_pos)

		# If there is an object there...
		if obj:
			# ...pick a different direction
			last_dir = random.randint(0, 7)


	# Move in the direction without anything in the way
	return (Action.MOVE, last_dir)


# Initial direction to try to move
last_dir = Direction.SOUTH

# Create our client
c = Client()

# Insert your key here
c.KEY = <key>

# Tell the client to use this function to decide the next move.
# This function is defined above.
c.decide_move = dummy

# Connect to the game server
if c.connect():
	# If we successfully connected, start playing
	print 'Connected'

	# Tell the client to start listening for maps
	c.start()

	# Wait until the user presses a key
	raw_input('Press any key to quit...')

	# Tell the client to stop listening for maps
	c.stop()

	# Wait for the client to finish its last request
	c.join()

	# Disconnect from the server
	c.disconnect()
else:
	# If we didn't successfully connected, exit
	print 'Could not connect'
