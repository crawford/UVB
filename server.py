#!/usr/bin/python

from controller import *
from connection import *
from logger import *
import select
import socket
import sys
import threading
import ConfigParser

PROMPT = "uvb> "

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
			self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			#self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.server.bind((self.host, self.port))
		except socket.error, (value, message):
			if self.server:
				self.server.close()
			logger.critical("Could not open socket: " + str(message))
			sys.exit(1)

	def run(self):
		logger.debug("Server started")
		self.running = True
		self.server.settimeout(self.server_timeout)
		self.server.listen(1)
		while self.running:
			try:
				socket, address = self.server.accept()
				p = Connection(socket)
				p.start()
				s.connections.append(p)
				logger.info("New connection from" + str(address))
			except:
				pass

			self.destroy_idle_connections()

	def load_config(self):
		logger.info("Loading server configuration...")
		config = ConfigParser.ConfigParser()
		config.read("config")

		self.maxplayers = int(config.get("Server", "MaxPlayers"))
		self.port = int(config.get("Server", "Port"))
		self.connection_backlog = int(config.get("Server", "Backlog"))
		gamewidth = int(config.get("GameBoard", "Width"))
		gameheight = int(config.get("GameBoard", "Height"))

		logger.info("Port: " + str(self.port))
		logger.info("Connection Backlog: " + str(self.connection_backlog))
		logger.info("Max Players: " + str(self.maxplayers))

		self.controller = Controller()

	def close(self):
		self.running = False
		logger.info("Waiting for server to close...")

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


logger = createLogger('Server')


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
		choice = raw_input(PROMPT)
		commands.get(choice, (command_unknown, 0))[0]()

	s.join()
	logger.info("Terminating")
	logger.debug("Server closed")
