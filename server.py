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
import ConfigParser

maxgamelength = 1000
maxdecisiontime = 5
maxplayers = 20
minvisibility = 5
maxvisibility = 10
gameheight = 50
gamewidth = 50

class Server:
    def __init__(self):
        self.host = socket.gethostname()
        self.port = 41294
        self.connection_backlog = 5
        self.size = 1024
        self.server = None
        self.players = []
        self.server_timeout = 5
        self.start_waittime = 10

        self.gameboard = None

    def open_server(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host, self.port))
            self.server.listen(self.connection_backlog)
        except socket.error, (value, message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)

    def get_players(self, waittime):
        # set the start time
        starttime = datetime.datetime.now() + waittime
        
        input = [self.server]
        running = True
        
        print "Waiting for new players..."
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

    def load_config(self):
        print "Loading configuration..."
        config = ConfigParser.ConfigParser()
        config.read("config")

        maxgamelength = int(config.get("Server", "MaxGameLength"))
        maxdecisiontime = int(config.get("Server", "MaxDecisionTime"))/1000
        maxplayers = int(config.get("Server", "MaxPlayers"))
        minvisibility = int(config.get("Server", "MinVisibility"))
        maxvisibility = int(config.get("Server", "MaxVisibility"))
        gamewidth = int(config.get("Server", "GameWidth"))
        gameheight = int(config.get("Server", "GameHeight"))

        print " Max Game Length:", maxgamelength
        print " Max Decision Time:", maxdecisiontime
        print " Max Players:", maxplayers
        print " Min Visibility:", minvisibility
        print " Max Visibility:", maxvisibility
        print " Game Height:", gameheight
        print " Game Width:", gamewidth
        
        self.gameboard = GameBoard(gamewidth, gameheight)

    def run(self):
        self.load_config()
        self.open_server()
        
        # get connections and wait for the start of the game
        self.get_players(datetime.timedelta(seconds=self.start_waittime))

        print "Starting game..."
        gamecount = 0

        # loop while the game hasn't run too long and there are still players
        while (gamecount < maxgamelength) and (len(self.players) > 1):
            # loop through all of the active players
                # create a derived gameboard for the specific player
                # send the gameboard to the player and ask for a move
                
            # apply all of the moves to the gameboard
                # if they moved, update their position on the map
                # if they made a snowball, increment their count
                # if they made a snowman, place a snowman on the map
                # if they threw a snowball, create a snowball in the direction on the map
            # check for any collisions between players and objects
                # if the player is in the same spot as another object, kill them
            pass
            #for p in self.players:
            #    p.join()

        print "Game finished, exiting..."




class Connection(threading.Thread):
    def __init__(self, (socket, address)):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.size = 1024
        self.operation
    
    def run(self):
        """running = True
        while running:
            data = self.socket.recv(self.size)
            if data:
                self.socket.send(data)
            else:
                self.socket.close()
                running = False
        """
        
        input = [self.socket]
        inready, outpready, exready = select.select(input, [], [], self.timeout)
            
        if len(inready) > 0:
            print "Received move from player at", self.address
        else:
            print "No response from player at", self.address

    def requestMove(self, map, timeout):
        print "Sending map to player at", self.address
        #send map
        self.timeout = timeout
        start()
        
        




if __name__ == "__main__":
    print " _     _ _     _ ______      ______                   _           _ _  "
    print "| |   | | |   | |  __  \    / _____)                 | |         | | | "
    print "| |   | | |   | | |__)  )  ( (____  ____   ___  _ _ _| |__  _____| | | "
    print "| |   | | |   | |  __  (    \____ \|  _ \ / _ \| | | |  _ \(____ | | | "
    print "| |___| |\ \ / /| |__)  )   _____) ) | | | |_| | | | | |_) ) ___ | | | "
    print " \_____/  \___/ |______/   (______/|_| |_|\___/ \___/|____/\_____|\_)_)"
    print ""
    
    s = Server()
    s.run()