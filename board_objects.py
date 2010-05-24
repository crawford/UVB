# Board Objects module

class BoardObject(object):
    """ Superclass for a board object

    Attributes:
        x - current x position
        y - current y position
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "-"

    def delete(self):
        del self.x
        del self.y

	def get_next_move(self):
		return (self.x, self.y)

    def move(self,x,y):
        self.x = x
        self.y = y

    def get_position(self):
        return (self.x,self.y)

    def get_XML(self):
        return "<" + self.__class__.__name__ + " x=\"" + str(self.x) + "\" y=\"" + str(self.y) + "\"></" + self.__class__.__name__ + ">"

'''
class BoardObstacle(BoardObject):
    """ Simple obstacle for the board

    Attributes:
        x - current x position
        y - current y position
    """
    def __str__(self):
        return "^"
'''
