#!/usr/bin/env python

import sys
import getopt
import Configuration

def usage (myself):
	print "Usage " + myself + " [OPTIONS]"
	print "  -h, --help\t\t\tthis help"
	print "  -c, --config <path>\t\tpath to configuration file"

def main (argv):
	try:
		opts, args = getopt.getopt (argv[1:], "c:h", ["config=", "help"])
	except getopt.GetoptError as ex:
		print ex
		usage (argv[0])
		sys.exit (1)
	
	configFile = None
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage (argv[0])
			sys.exit (0)
		elif opt in ("-c", "--config"):
			configFile = arg
	
	if not configFile:
		print "missing required option: --config <path>"
		sys.exit(1)
	
	try:
		config = Configuration.Configuration(configFile)
	except Configuration.ConfigurationException as ex:
		print "Error: " + ex.args[0]
		sys.exit(1)
	
	print "Using bin path: " + config.getBinPath()

if __name__ == "__main__":
	main (sys.argv)
