#!/usr/bin/python

import socket
import threading
import sys 			# Support command line args
import getopt 		# Support command line option parsing
import os			# Kill the application
import signal		# Catch an interrupt
import time			# Thread sleeping

# Global variables definitions

target = "" 
port = False
listen = False
command = ""
upload = False


# This tool should be able to replace netcat

# The tool should be able to act as a server and as a client depending on the arguments

###############################################################################
# Start menu
def menu():
	print "pycat, a python implementation of netcat"
	print ""
	print "Usage:"
	print ""
	print "-h, --help:    Display this menu"
	print "-t, --target:  The IP to bind to"
	print "-l, --listen:  Listen mode (act as a server)"
	print "-p, --port:    The port number to bind to"
	print "-c, --command: The command you wish to execute via pycat"
	print "-u --upload:   Set this flag to upload a file"
	print ""
	print ""
	print "By default, pycat will act as a client unless the -p flag is specified"
	print ""
	print "Examples will happen later..."
	print ""

	sys.exit(0)

###############################################################################
# Connect as a client
def connectMode(client_socket, address):

	global kill_thread

	# Get raw input which is terminated with \n
	try:

		while True:

			buffer = raw_input()
			buffer += "\n"

			if buffer == "quit\n" or buffer == "q\n":
				client_socket.close()
				sys.exit(0)

			if not client_socket:
				print "[!!] No connection on the other end!"
				client_socket.close()
				break				

			client_socket.send(buffer)

	except Exception as err:
		print "[!!] Caught exception in client thread: %s!" % err
		client_socket.close()

###############################################################################
# Handle the connection from the client.
def handle_client(client_socket, address):

	print "[*] Got a connection from %s:%d" % (address[0], address[1]) 

	try:
		while True:
			# Wait for a response
			request = client_socket.recv(4096)	

			# If the client disconnects, request is 0
			if not request:
				break

			# Output what the client has given us
			print request

		client_socket.close()

	except Exception as err:
		print "[!!] Caught exception in server thread: %s" % err
		client_socket.close()
		sys.exit(0)

###############################################################################
# This is the listening functionality of the program
def serverMode():

	global target
	global port
	
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	if not len(target):
		target = "0.0.0.0"

	try:
		server.bind((target, port))
	except socket.error as err:
		print err
		sys.exit(0)

	server.listen(5)
	print "[*] Listening on %s:%d" % (target, port)



	while True:
	
		try:
		
			# This will wait until we get a connection
			client, address = server.accept()


			# Create a thread to handle incoming responses 
			# Daemonic threads will die as soon as the main thread dies
			listen_thread = threading.Thread(target = handle_client, args = (client, address))
			listen_thread.daemon = True
			listen_thread.start()	
			# Create a thread to handle outgoing requests
			client_thread = threading.Thread(target = connectMode, args = (client, address))
			client_thread.daemon = True
			client_thread.start()	


			time.sleep(1)

			'''
			# The problem is that python does NOT pass by refernece!
			This means that the sockets are simply copies and the actual socket that gets closed
			does not do anything!
			'''
		except (KeyboardInterrupt, SystemExit):
			print "Cleaning up sockets..."
			client.close()
			sys.stdout.write("Exiting form main thread...\n")
			sys.exit(0)
		
###############################################################################
# main definition
def main():
	
	global target
	global listen
	global port
	global command
	global upload


	# Set the option
	# If the options are not parsing properly, then try gnu_getopt

	if not len(sys.argv[1:]):
		menu()

	try:
		options, remainder = getopt.getopt(sys.argv[1:], 'ht:lp:cu', ['help', 'target', 'listen', 'port', 'command', 'upload'])

	except getopt.GetoptError as err:
		print str(err)
		menu()
						
	for opt, arg in options:
		if opt in ('-h', '--help'):
			menu()
		elif opt in ('-t', '--target'):
			target = arg
		elif opt in ('-l', '--listen'):
			listen = True
		elif opt in ('-p', '--port'):
			port = int(arg)
		elif opt in ('-c', '--command'):
			command = arg
		elif opt in ('-u', '--upload'):
			upload = True
		else:
			assert False, "Invalid option" # This throws an error

	print "Target: %s" % target
	print "Listen: %s" % listen
	print "Port: %d" % port

	if port > 0:
		if not listen and len(target):
			print "Client mode"
		elif listen:
			serverMode()
		else:					# This could probably be cleaned up a little since the functions will have looping
			menu()
	else:
		menu()

###############################################################################
# Program execution

try:
	main()
except KeyboardInterrupt:
	print ""
	sys.exit(0)
