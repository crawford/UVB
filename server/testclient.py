#!/usr/bin/python

from client import Client
from constants import Action, Direction

def dummy(junk):
	return (Action.MOVE, Direction.SOUTHEAST)


c = Client()

c.KEY = 'P6X6qeCysSj4xx2TeRC0OtJ46bWOsZDi'
c.decide_move = dummy
c.connect()
c.start()

raw_input('Press any key to quit...')

c.stop()
c.disconnect()





'''import socket
import select
import ssl

SERVER = 'uvb.csh.rit.edu'
PORT = 13783

if __name__ == "__main__":
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(5)
	sock = ssl.wrap_socket(sock, ca_certs="opcomm.crt", cert_reqs=ssl.CERT_REQUIRED)
	sock.connect((SERVER, PORT))

	inready, outready, exready = select.select([], [sock], [], 5)

	if outready:
		sock.send("P6X6qeCysSj4xx2TeRC0OtJ46bWOsZDi")


	a = raw_input('d')

	sock.close()'''