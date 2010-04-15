# UVB XML Game Board Parser

from xml.sax import saxutils
from board_objects import *
# Parser module for UVB Game Board XML

class ParseGameBoard(saxutils.DefaultHandler):
    def __init__(self):
        pass

    def startElement(self, name, attrs):
        # python lacks switch-case, so use if-elif
        x = attrs.get('x',None)
        y = attrs.get('y',None)
        if(name=="Snowball"):
            pass
        elif(name=="BoardObstacle"):
            pass
        elif(name=="Snowman"):
            pass
        elif(name=="Player"):
            name = attrs.get('name',None)
            print "Player at x: " + str(x) + " y: " + str(y) + " name: " + name

from xml.sax import make_parser
from xml.sax.handler import feature_namespaces

if __name__ == '__main__':
    # Create a parser
    parser = make_parser()
    # Tell the parser we are not interested in XML namespaces
    parser.setFeature(feature_namespaces, 0);
    # Create the handler
    dh = ParseGameBoard(board)
    parser.setContentHandler(dh)
    parser.parse('test.xml')
