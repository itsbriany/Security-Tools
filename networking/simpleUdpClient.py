#!/usr/bin/python

import socket

# Simple UDP client

target_host = "127.0.0.1"
target_port = 80

# Get a handle on a socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send some data
client.sendto("Here is some data for you", (target_host, target_port))

# Revieve a response
data, addr = client.recvfrom(4096)

print data

'''
To test this, you can set the -u flag on netcat
'''
