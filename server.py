#!/usr/bin/python

from controller import *
from connection import *
import select
import socket
import SocketServer
import sys
import threading
import ConfigParser

class TCPHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		global s
		if len(s.connections) <= s.maxplayers:
			# create a new connection to a client
			p = Connection(self.request)
			p.start()
			s.connections.append(p)
			print " New connection from", self.request.getpeername()




class Server(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

		self.host = socket.gethostname()
		self.port = 13783
		self.connection_backlog = 5
		self.size = 1024
		self.server = None
		self.connections = []
		self.server_timeout = 5
		self.maxplayers = 100
		self.controller = None
		self.running = False

	def open_server(self):
		try:
			self.server = SocketServer.TCPServer((self.host, self.port), TCPHandler)
		except socket.error, (value, message):
			if self.server:
				self.server.close()
			print "Could not open socket: " + message
			sys.exit(1)

		print "Sever opened"

	def run(self):
		self.running = True
		self.server.timeout = self.server_timeout
		while self.running:
			self.server.handle_request()
			self.destroy_idle_connections()

	def load_config(self):
		print "Loading server configuration..."
		config = ConfigParser.ConfigParser()
		config.read("config")

		self.maxplayers = int(config.get("Server", "MaxPlayers"))
		self.port = int(config.get("Server", "Port"))
		self.connection_backlog = int(config.get("Server", "Backlog"))
		gamewidth = int(config.get("GameBoard", "Width"))
		gameheight = int(config.get("GameBoard", "Height"))

		print " Port:", self.port
		print " Connection Backlog:", self.connection_backlog
		print " Max Players:", self.maxplayers

		self.controller = Controller()

	def close(self):
		self.running = False
		print "Waiting for server to close..."

	def destroy_idle_connections(self):
		i = 0
		while i < len(self.connections):
			if not self.connections[i].is_alive():
				self.connections[i].close()
				del self.connections[i]
			else:
				i = i+1




def command_help():
	for c in commands:
		print "\t", c, "\t\t", commands[c][1]

def command_quit():
	global running
	running = False
	s.close()

def command_players():
	print len(s.connections), " player(s)"

def command_unknown():
	print "Unknown command.  Type 'help' for commands."


if __name__ == "__main__":
	print " _     _ _     _ ______      ______                   _           _ _  "
	print "| |   | | |   | |  __  \    / _____)                 | |         | | | "
	print "| |   | | |   | | |__)  )  ( (____  ____   ___  _ _ _| |__  _____| | | "
	print "| |   | | |   | |  __  (    \____ \|  _ \ / _ \| | | |  _ \(____ | | | "
	print "| |___| |\ \ / /| |__)  )   _____) ) | | | |_| | | | | |_) ) ___ | | | "
	print " \_____/  \___/ |______/   (______/|_| |_|\___/ \___/|____/\_____|\_)_)"
	print ""

	s = Server()
	s.load_config()
	s.open_server()
	s.start()

	commands = {"help":(command_help, "Shows this message"),
				"exit":(command_quit, "See 'quit'"),
				"quit":(command_quit, "Shuts down the server, closes all connections, and terminates"),
				"players":(command_players, "Show the number of connected players")}

	running = True

	while running:
		choice = raw_input("uvb> ")
		commands.get(choice, (command_unknown, 0))[0]()

	s.join()
	print "Terminating"
