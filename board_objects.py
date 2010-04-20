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

    def move(self,x,y):
        self.x = x
        self.y = y

    def getPostion(self):
        return (self.x,self.y)

    def getXML(self):
        return "<" + self.__class__.__name__ + " x=\"" + str(self.x) + "\" y=\"" + str(self.y) + "\"></" + self.__class__.__name__ + ">"

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

    def getXML(self):
        return "<" + self.__class__.__name__ + " x=\"" + str(self.x) + "\" y=\"" + str(self.y) + "\" owner=\"" + self.owner + "\" direction=\"" + self.direction +"\"></" + self.__class__.__name__ + ">"

class BoardObstacle(BoardObject):
    """ Simple obstacle for the board

    Attributes:
        x - current x position
        y - current y position
    """
    def __str__(self):
        return "^"

class Snowman(BoardObstacle):
    """ Simple obstacle for the board

    Attributes:
        x - current x position
        y - current y position
    """
    def __str__(self):
        return "8"

class Player(BoardObject):
    """ Represents the player on the game board

    Attributes:
        x - current x position
        y - current y position

        name - player name
        snowballs - number of snowballs the player has
    """

    def __init__(self, x, y, name, snowballs=None):
        if(snowballs==None):
            self.snowballs = 0
        self.name = name
        super(Player,self).__init__(x,y)

    def throwSnowball():
        if(self.snowballs > 0):
            self.snowballs = self.snowballs - 1
            return true
        else:
            return false

    def __str__(self):
        return self.name

    def getXML(self):
        return "<" + self.__class__.__name__ + " x=\"" + str(self.x) + "\" y=\"" + str(self.y) + "\" name=\"" + self.name + "\"></" + self.__class__.__name__ + ">"
