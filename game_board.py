# GameBoard class module

import random
from board_objects import *

class GameBoard(object):
    """ GameBoard object for UVB-AI

    Attributes:
        width - width of the board
        height - height of the board
        board - actual game board

        players - list of players
        activePlayers - list of players still alive

    Methods:
        update - update (advance) the game board
        getXML - return XML represenation of the game board
    """

    def __init__(self, width, height, players=None):
        self.width = width
        self.height = height
        if(players == None):
            self.players = []
            self.activePlayers = []
        else:
            self.players = players
            self.activePlayers = players
        self.board = []

        for y in range(height):
            self.board.append([])
            for x in range(width):
                self.board[y].append(BoardObject(x,y));
        if(players != None):
            for p in players:
                placed = False
                while not placed:
                    x = random.randrange(0,width)
                    y = random.randrange(0,height)
                    if( self.board[y][x].__class__ is not BoardObject):
                        continue
                    placed = True
                    self.board[y][x].delete
                    print "x: " + str(x) + " y: " + str(y)
                    p.move(x,y)
                    self.board[y][x] = p

    # add an object to the game board
    def addObject(self,boardObject):
        if(self.board[boardObject.y][boardObject.x].__class__ is not BoardObject):
            raise IllegalPostion(x,y)
        else:
            self.board[boardObject.y][boardObject.x] = boardObject
            # If it's a player, add player to the player lists
            if(boardObject.__class__ is Player):
                self.players.append(boardObject)
                self.activePlayers.append(boardObject)

    # remove an object from the game board
    def removeObject(self,boardObject):
        pass

    # update the game board state
    def update(self):
        pass

    # convert the game board to a string
    def __str__(self):
        strang = ""
        for i in range(self.height):
            for j in range(self.width):
                strang += self.board[i][j].__str__() + " "
            strang += "\n"
        return strang

    # return XML representation of the game board
    def getXML(self):
        strang = "<board width=\"" + str(self.width) + "\" height=\"" + str(self.height) + "\">\n"
        for i in range(self.height):
            for j in range(self.width):
                if( self.board[i][j].__class__ is BoardObject):
                    continue
                strang += "\t" + self.board[i][j].getXML() + "\n"
        strang += "</board>"
        return strang

# Class to represent an IllegalPosition Exception
class IllegalPosition(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)
