#!/usr/bin/env python

import sys
import getopt
import time
import signal
import Queue
import Configuration
import ProcessExecutor
import ServerProcess
import ServerApi
import HttpJsonApi


api = None
def signal_handler(signal, frame):
	print "You pressed Ctrl+C!"
	api.quit()

def usage (myself):
	print "Usage " + myself + " [OPTIONS]"
	print "  -h, --help\t\t\tthis help"
	print "  -c, --config <path>\t\tpath to configuration file"

def main (argv):
	global api
	
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
	
	print "Configuration:"
	print "\tbinPath: " + config.getBinPath()
	print "\tbinArgs: " + repr (config.getBinArgs())
	
	print "Registering signal handler"
	signal.signal(signal.SIGINT, signal_handler)
	
	executor = ProcessExecutor.ProcessExecutor (config.getBinPath(), config.getBinArgs())
	server = ServerProcess.ServerProcess (executor)
	api = ServerApi.ServerApi (server)
	httpJsonApi = HttpJsonApi.HttpJsonApi (api, "0.0.0.0", 1234)
	httpJsonApi.start()
	
	#signal.pause()
	while not api.waitForQuit(1):
		pass
	httpJsonApi.stop()
	
	print "Good bye!"

if __name__ == "__main__":
	main (sys.argv)
