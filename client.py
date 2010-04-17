#!/usr/bin/python
# A very simple AI challenge game written by David Brenner for CSH (csh.rit.edu)
"""
It's a snowball fight! The rules are as follows.

Each turn, a player can:
    Do nothing
    Move in a direction
    Make a snowball
    Throw a snowball in a direction
    Build a snowman  in a direction

Actions that require a direction can be done in the cardinal or intermediate 
    directions (N, S, E, W, NE, NW, SW, SE).

Invalid actions result in inaction. These include:
    Moving somewhere where you can't move
    Throwing a snowball when you don't have one

Snowmen are stationary shields. They are destroyed by collision with a player
    or snowball.

When a player loses, the player is removed from the game.

Players lose by:
    Colliding into one another (both players lose)
    Getting hit by a snowball

Players win by:
    Being the last in the game

"""

# Main module

from game_board import *

SERVER = "blahblahblah"
PORT = "blah"

if __name__ == "__main__":
    print "main"

class Client

	xPos = 0
	yPos = 0

	obstacleList = []
	
	def connect() :
	
	def parse(String XML) :

	def getMove(BoardObject board) :
		objects = board.getArray()

		currClosest = sys.maxint

		for boardObject in objects :
			if boardObject.__class__ is BoardObstacle 
				&& !contains( obstacleList , lambda x : x == boardObject ) :
				obstacleList.add( boardObject )
			else if boardObject.__class__ is Player : 
				if getDistance( boardObject.x , boardObject.y ) < currClosest :
					closestPlayer = boardObject


				
			
	def getDistance(x , y) :
		return Math.sqrt( ( xPos - x ) ** 2 + ( yPos - y ) ** 2 )  

	def getDirection(x , y) :
		if xPos - x == 0 :
			if  yPos - y == 0 : 
				return 0 , 0
			else return 0 , yPos - y / Math.abs( yPos - y )
		else 
			if yPos - y == 0 :
				return xPos - x / Math.abs( xPos - x ) , 0
			else return xPos - x / Math.abs( xPos - x ) , yPos - y / Math.abs( yPos - y )

	def contains(list , filter)
		for x in list : 
			if filter(x) : 
				return True
		else return False
		
