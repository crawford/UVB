# GameBoard class module

import random
from board_objects import *

class GameBoard(object):
    """ GameBoard object for UVB-AI

    Attributes:
        width  - width of the board
        height - height of the board

        players   - list of players
        snowballs - list of moving snowballs
        board     - actual game board

    Methods:
        addObject       - adds and object to the board
        removeObject    - remove an object from the board
        moveObject      - moves an object

        getVisibleBoard - returns a new board given a (x,y) coordinate and radius
        getXML          - returns XML represenation of the game board
        __str__         - returns string represenation of the game board
    """

# dictionary of players
# list of snowballs
# "game board" 2d list
# createMaskVisibleBoard(self,x,y,radius)
#
#
# gameController - moves people, updates board, etc.
# - isGameOver
# - step (advance game)
#   snowball speed configuration

    def __init__(self, width, height, players=None):
        self.width = width
        self.height = height
        self.players = {}
        self.snowballs = []
        self.board = [[] for i in range(width)]

    # get object at (x,y) coordinate
    def getObject(self,x,y):
        if( len(self.board[x]) == 0 ):
            return False
        for i in range( len(self.board[x]) ):
            if(i.y == y):
                return i
            elif(i.y > y):
                return False

    # add an object to the game board
    def addObject(self,boardObject):
        cur = getObject(boardObject.x,boardObject.y)
        if( cur != False):
            # return false if there's already something there
            return False
        else: 
            # check if snowball or player
            if(boardObject.__class__ is Snowball):
                # add to snowball list
                self.snowballs.append(boardObject)
            elif(boardObject.__class__ is Player):
                # add to player dictionary
                self.players[boardObject.ID] = boardObject

            # add to the actual game board
            if( len(self.board[boardObject.x] == 0) ): 
                # append if list is empty
                self.board[boardObject.x].append(boardObject);
            else:
                inserted = False
                for i, value in enumerate(self.board[x]):
                    if(i > y):
                        inserted = True
                        self.board[boardObject.x].insert(i,boardObject)
                        break
                if(not inserted):
                    self.board[boardObject.x].append(boardObject)

    # remove an object from the game board
    def removeObject(self,boardObject):
        # check if snowball or player
        if(boardObject.__class__ is Snowball):
            # remove from snowball list
            self.snowballs.remove(boardObject)
        elif(boardObject.__class__ is Player):
            # remove from player dictionary
            del self.players[boardObject.ID]
        self.board[boardObject.x].remove(boardObject)

    # move an object on the game board
    def moveObject(self,boardObject,x,y):
        #TODO: make this more efficient
        self.removeObject(boardObject)
        boardObject.x = x
        boardObject.y = y
        self.addObject(boardObject)

    def getVisibleBoard(self,x,y,radius):
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
