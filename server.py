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
        self.players = []
        self.server_timeout = 5
        self.start_waittime = 10

    def open_server(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host, self.port))
            self.server.listen(self.backlog)
        except socker.error, (value, message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)

    def get_players(self, waittime):
        # set the start time
        starttime = datetime.datetime.now() + waittime
        
        input = [self.server]
        running = True
        
        print "Listening for new players..."
        while running:
            inready, outpready, exready = select.select(input, [], [], self.server_timeout)

            for s in inready:
                # create a new connection to a client
                p = Connection(self.server.accept())
                p.start()
                self.players.append(p)
                    
                print " New player at ", p[1]

            # if the current time has passed the start time, close the server
            if datetime.datetime.now() > starttime:
                running = False

        self.server.close()
        print "Server closed -", len(self.players), " players"

    def run(self):
        self.open_server()
        
        # get connections and wait for the start of the game
        self.get_players(datetime.timedelta(seconds=self.start_waittime))

        for p in self.players:
            p.join()

class Connection(threading.Thread):
    def __init__(self, (socket, address)):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.size = 1024
    
    def run(self):
        running = 1
        while running:
            data = self.socket.recv(self.size)
            if data:
                self.socket.send(data)
            else:
                self.socket.close()
                running = 0


if __name__ == "__main__":
    print "main"
    players = [Player(0,0,"P"), Player(0,0,"T")]
    board = GameBoard(5,10,players)
    print board.__str__()
    s = Server()
    s.run()