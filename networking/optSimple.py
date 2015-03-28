#!/usr/bin/python

# Simple getopt module program for argument parsing

import sys
import getopt

version = '1.0'
verbose = False
output_filename = 'default.out'

# The colon appended to the argcount means go from that index to the end
print 'ARGV      :', sys.argv[1:]

# options indicate the expected options given. remainder is everything else
'''
The first parameter indicates the arguments to set
The second parameter indicates the flag abbreviations. If there is a colon appended, then
	that parameter MUST take a value as a parameter.
The third parameter indicates the expanded form of the flag.
'''
options, remainder = getopt.getopt(sys.argv[1:], 'o:v', ['output=','verbose','version=',])

print 'OPTIONS   :', options

try: 
	for opt, arg in options:
		if opt in ('-o', '--output'):
			output_filename = arg
		elif opt in ('-v', '--verbose'):
			verbose = True
		elif opt == '--version':
			version = arg


	print 'VERSION   : %s ' % version
	print 'VERBOSE   : %s ' % verbose
	print 'OUTPUT    : %s ' % output_filename
	print 'REMAINING : %s ' % remainder

except:
	print "Error!"
	print sys.stderr.read()
