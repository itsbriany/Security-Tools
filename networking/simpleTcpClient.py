#!/usr/bin/python

# This is a simple TCP client script

import socket

# Targets
targetHost = "0.0.0.0"
targetPort = 9999 

# Socket fd with Ipv4 and TCP connection 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to www.google.ca:80
# Notice that this takes a structure as a parameter
client.connect((targetHost, targetPort))

# Send some data
client.send("GET HTTP/1.1\r\nHost: google.com\r\n\r\n")

# Get the response (max 4096 bytes)
response = client.recv(4096)

print response

# The spam loop
'''
for x in range(0,5):
	client.send("GET HTTP/1.1\r\nHost: google.com\r\n\r\n")
	response = client.recv(4096)
	print response
'''
