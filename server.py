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

class Server:
    def __init__(self):
        self.host = ''
        self.port = 88888
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []

    def open_socket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host,self.port))
            self.server.listen(5)
        except socker.error, (value,message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)

    def run(self):
        self.open_socket()
        input = [self.server,sys.stdin]
        running = 1
        while running:
            inputready,outputready,exceptready = select.select(input,[],[])

            for s in inputready:
                if s == self.server:
                    # handle the server socket
                    c = Client(self.server.accept())
                    c.start()
                    self.threads.append(c)
                elif s == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0
        # close all threads

        self.server.close()
        for c in self.threads:
            c.join()

class Client(threading.Thread):
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
