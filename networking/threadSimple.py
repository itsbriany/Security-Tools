#!/usr/bin/python

# Simple threading program

import time
import threading

def printChars():
	for x in range(0,10):
		print x	

def printLines():
	for x in range(0,10):
		print "Hello Thread!"
		time.sleep(1)
		
t1 = threading.Thread(target = printChars)
t2 = threading.Thread(target = printLines)
t1.start()
t2.start()
