#!/usr/bin/python

from client import Client
from constants import Action, Direction
import random

def dummy(board):
	global last_dir

	print board

	#obj = 1
	#while obj:
	#	next_pos = board.next_pos_in_direction((0, 0), last_dir)
	#	obj = board.get_object_at(next_pos)
	#	if obj:
	#		last_dir = random.randint(0, 7)

	return (Action.THROWSNOWBALL, Direction.SOUTHEAST)



last_dir = Direction.SOUTH

c = Client()

c.KEY = 'P6X6qeCysSj4xx2TeRC0OtJ46bWOsZDi'
c.decide_move = dummy
c.connect()
c.start()

raw_input('Press any key to quit...')

c.stop()
c.join()
c.disconnect()
