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
import select
import socket
import sys
import threading
import datetime

class Server:
    def __init__(self):
        self.host = socket.gethostname()
        self.port = 41294
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.connections = []
        self.server_timeout = 5
        self.start_waittime = 300

    def open_server(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host,self.port))
            self.server.listen(self.backlog)
        except socker.error, (value,message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)

    def getconnections(self, waittime):
        starttime = datetime.datetime.now() + waittime
        input = [self.server,sys.stdin]
        running = 1
        while running and starttime > datetime.datetime.now():
            inputready,outputready,exceptready = select.select(input,[],[], self.server_timeout)

            for s in inputready:
                if s == self.server:
                    # handle the server socket
                    c = Connection(self.server.accept())
                    c.start()
                    self.connections.append(c)
                elif s == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0
                    
        self.server.close()

    def run(self):
        self.open_server()
        self.getconnections(self.start_waittime)

        for c in self.threads:
            c.join()

class Connection(threading.Thread):
    def __init__(self,(client,address)):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024
    
    def run(self):
        running = 1
        while running:
            data = self.client.recv(self.size)
            if data:
                self.client.send(data)
            else:
                self.client.close()
                running = 0


if __name__ == "__main__":
    print "main"
    players = [Player(0,0,"P"), Player(0,0,"T")]
    board = GameBoard(5,10,players)
    print board.__str__()
    s = Server
    s.run()
