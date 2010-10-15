#!/usr/bin/python

from controller import *
from connection import *
from player import *
from logger import *
import select
import socket
import sys
import threading
import ConfigParser

PROMPT = "uvb> "

class Server(threading.Thread):
	host = None
	port = None
	connection_backlog = None
	size = None
	server = None
	anon_conns = None
	server_timeout = None
	maxplayers = None
	controller = None
	running = None
	logger = None

	def __init__(self):
		threading.Thread.__init__(self)

		self.host = socket.gethostname()
		self.port = 13783
		self.connection_backlog = 5
		self.size = 1024
		self.server = None
		self.anon_conns = []
		self.players = []
		self.server_timeout = 5
		self.maxplayers = 100
		self.controller = None
		self.running = False
		self.logger = create_logger('Server')

	def open_server(self):
		try:
			self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			#self.server.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
			#self.server.setsockopt(socket.SOL_SOCKET, socket.TCP_KEEPCNT, 3)
			#self.server.setsockopt(socket.SOL_SOCKET, socket.TCP_KEEPIDLE, 5)
			#self.server.setsockopt(socket.SOL_SOCKET, socket.TCP_KEEPINTVL, 1)

			self.server = ssl.wrap_socket(self.server, 
											keyfile='/etc/ssl/private/uvb_key.pem', 
											certfile='/etc/ssl/certs/uvb_cert.pem', server_side=True)
			self.server.bind((self.host, self.port))
		except socket.error, (value, message):
			self.logger.critical("Could not open socket: " + str(message))
			if self.server:
				self.server.close()
			sys.exit(1)

	def run(self):
		self.logger.debug("Server started")
		self.running = True
		self.server.settimeout(self.server_timeout)
		self.server.listen(self.connection_backlog)

		while self.running:
			try:
				rsocket, address = self.server.accept()

				# Try to get the hostname, otherwise just use the IP address
				try:
					hostname, aliases, iplist = socket.gethostbyaddr(address[0])
				except socket.herror:
					hostname = address[0]

				self.logger.info("New connection from " + str(hostname) + " " + str(rsocket.cipher()))
				p = Connection(rsocket, hostname, self)
				p.authenticate()
				s.anon_conns.append(p)
			except socket.timeout:
				pass

			self.destroy_idle_connections()

	def load_config(self):
		self.logger.info("Loading server configuration...")
		config = ConfigParser.ConfigParser()
		config.read("config")

		self.maxplayers = int(config.get("Server", "MaxPlayers"))
		self.port = int(config.get("Server", "Port"))
		self.connection_backlog = int(config.get("Server", "Backlog"))
		gamewidth = int(config.get("GameBoard", "Width"))
		gameheight = int(config.get("GameBoard", "Height"))

		self.logger.info("Port: " + str(self.port))
		self.logger.info("Connection Backlog: " + str(self.connection_backlog))
		self.logger.info("Max Players: " + str(self.maxplayers))

		self.controller = Controller()

	def create_player(self, username, connection):
		self.logger.debug("Creating player: " + username)
		player = self.controller.get_player(username)
		if player:
			#player is already in game
			self.logger.info("Detected " + username + " cheating (multiple instances)")
			player.disconnect()
			connection.close()
			#flag this user as cheating
			return

		player = self.controller.create_player(username, connection)
		connection.logger = player.logger

		# Remove the connection from the list of anonymous connections
		self.anon_conns.remove(connection)

		# Add the player to the list of players
		self.players.append(player)
		self.controller.add_player(player)

	def close(self):
		self.running = False
		self.controller.stop()
		self.logger.info("Waiting for server to close...")

	def destroy_idle_connections(self):
		i = 0
		while i < len(self.anon_conns):
			if not self.anon_conns[i].is_running():
				self.anon_conns[i].close()
				self.logger.info("Removing idle connection to " + str(self.anon_conns[i].hostname))
				del self.anon_conns[i]
			else:
				i = i+1

		i = 0
		while i < len(self.players):
			if not self.players[i].connection.is_running():
				self.players[i].disconnect()
				self.controller.remove_player(self.players[i])
				self.logger.info("Removing idle connection to " + str(self.players[i].username))
				del self.players[i]
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
	print len(s.players), " player(s)"

def command_unknown():
	print "Unknown command.  Type 'help' for commands."




if __name__ == '__main__':
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

	commands = {'help':(command_help, "Shows this message"),
				'exit':(command_quit, "See 'quit'"),
				'quit':(command_quit, "Shuts down the server, closes all connections, and terminates"),
				'players':(command_players, "Show the number of connected players")}

	running = True

	while running:
		choice = raw_input(PROMPT)
		commands.get(choice, (command_unknown, 0))[0]()

	s.join()
	s.logger.debug("Server closed")
