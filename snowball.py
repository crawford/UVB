from board_objects import *

class Snowball(BoardObject):
    """ Represents a snowball object

    Attributes:
        x - current x position
        y - current y position
        direction - heading for the direction the snowball is traveling in
    """

    def __init__(self, x, y, direction, owner):
        self.direction = direction
        self.owner = owner
        super(Snowball,self).__init__(x,y)

	def __str__(self):
		return 'O'

    def get_XML(self):
        return "<" + self.__class__.__name__ + " x=\"" + str(self.x) + "\" y=\"" + str(self.y) + "\" owner=\"" + self.owner + "\" direction=\"" + self.direction +"\"></" + self.__class__.__name__ + ">"
