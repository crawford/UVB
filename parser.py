# UVB XML Game Board Parser

from xml.sax import saxutils
from board_objects import *
from game_board import *
# Parser module for UVB Game Board XML

class ParseGameBoard(saxutils.DefaultHandler):
    def __init__(self):
        self.board = None

    def startElement(self, name, attrs):
        # python lacks switch-case, so use if-elif
        if(name=="board"):
            width  = int( attrs.get('width',None) )
            height = int( attrs.get('height',None) )
            self.board = GameBoard(width,height)
        else:
            x = int( attrs.get('x',None) )
            y = int( attrs.get('y',None) )
            if(name=="Snowball"):
                direction = attrs.get('direction',None)
                self.board.addObject( Snowball(x,y,direction) )
            elif(name=="BoardObstacle"):
                self.board.addObject( BoardObstacle(x,y) )
            elif(name=="Snowman"):
                self.board.addObject( Snowman(x,y) )
            elif(name=="Player"):
                name = attrs.get('name',None)
                self.board.addObject( Player(x,y,name) )

from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from board_objects import *
from game_board import *

class GameBoardParser(object):
    def __init__(self):
        # Create a parser
        self.parser = make_parser()
        # Tell the parser we are not interested in XML namespaces
        self.parser.setFeature(feature_namespaces, 0);
        # Create the handler
        self.dh = ParseGameBoard()
        self.parser.setContentHandler(self.dh)

    def parse(self,XMLstring):
        self.parser.parseString(XMLstring)
        print dh.board.__str__()
        return self.dh.board

if __name__ == '__main__':
    # Create a parser
    parser = make_parser()
    # Tell the parser we are not interested in XML namespaces
    parser.setFeature(feature_namespaces, 0);
    # Create the handler
    dh = ParseGameBoard()
    parser.setContentHandler(dh)
    parser.parse('test.xml')
    print dh.board.__str__()
