#!/usr/bin/python

from client import Client
from constants import Action, Direction
import random

def dummy(board):
	global last_dir

	print board

	return (Action.THROWSNOWBALL, Direction.SOUTHEAST)



last_dir = Direction.SOUTH

c = Client()

c.KEY = <key>
c.decide_move = dummy
c.connect()
c.start()

raw_input('Press any key to quit...')

c.stop()
c.join()
c.disconnect()
