#!/usr/bin/python

import socket
import threading

bindIp = "0.0.0.0"
bindPort = 9999

# A simple TCP server

# Get a handle on the socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the port
server.bind((bindIp, bindPort))

# Wait for client connection
server.listen(5)

print "[*] Listening on %s:%d" % (bindIp, bindPort)


# Processes
def handle_client(client_socket):
	
	# Get the request from the client
	request = client_socket.recv(4096)

	print "[*] <=== Incoming request: "
	print "%s" % request

	# Give the client a response 
	answer = "Hello from simple TCP server!\r\n"
	response = client_socket.send(answer)
	print "[*] ===> Responded to client with the following message: "
	print answer


	# Close the connection
	client_socket.close()
	


while True:
	client_connection, addr = server.accept()
 	print "[*] Accepted connection from: %s:%d" % (addr[0], addr[1])	

	# We will use a thread for the client's connection so that this program will run faster
	# Note that we need to override the constructor to run a process.Processes are defined below...

	'''
	The Thread takes the process as the first parameter and then args indicates the
	arguments for the given process. Note that in python, everything needs to be
	defined before they are used.
	'''

	client_thread = threading.Thread(target = handle_client, args = (client_connection, ))
	client_thread.start()
