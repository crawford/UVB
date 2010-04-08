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
    """

    def __init__(self, width, height, players):
        self.width = width
        self.height = height
        self.players = players
        self.activePlayers = players
        self.board = []

        for y in range(height):
            self.board.append([])
            for x in range(width):
                self.board[y].append(BoardObject(x,y));
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


    def __str__(self):
        str = ""
        for i in range(self.height):
            for j in range(self.width):
                str += self.board[i][j].__str__() + " "
            str += "\n"
        return str


    def update(self):
        pass
