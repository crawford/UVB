#!/usr/bin/python

from client import Client
from constants import Action, Direction
import random

def dummy(board):
	global last_dir
	global toggle

	print board

	toggle = not toggle
	if toggle:
		return (Action.THROWSNOWBALL, Direction.EAST)
	else:
		return (Action.MAKESNOWBALL, Direction.NORTH)



toggle = True
last_dir = Direction.SOUTH

c = Client()

#c.KEY = <key>
c.KEY = 'P6X6qeCysSj4xx2TeRC0OTJ46bWOsZDi'
c.decide_move = dummy
c.connect()
c.start()

raw_input('Press any key to quit...')

c.stop()
c.join()
c.disconnect()
