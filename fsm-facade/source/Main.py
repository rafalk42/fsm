#!/usr/bin/env python

import sys
import getopt
import time
import signal
import Configuration
import ProcessExecutor

executor = None
def signal_handler(signal, frame):
	print "You pressed Ctrl+C!"
	stdinQueue = executor.getStdinQueue()
	stdinQueue.put ("/quit")
	executor.wait()
	print "Process quit"

def usage (myself):
	print "Usage " + myself + " [OPTIONS]"
	print "  -h, --help\t\t\tthis help"
	print "  -c, --config <path>\t\tpath to configuration file"

def main (argv):
	global executor
	signal.signal(signal.SIGINT, signal_handler)
	
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
	
	executor = ProcessExecutor.ProcessExecutor (config.getBinPath())
	executor.start()
	stdoutQueue = executor.getStdoutQueue()
	stdinQueue = executor.getStdinQueue()
	
	time.sleep(0.5)
	
	#lines = executor.readLines()
	#for line in lines:
	#	print "OUT: " + line
	#executor.writeLine ("/time")
	#time.sleep (0.1)
	#executor.writeLine ("/quit")
	#while executor.isRunning():
	#	lines = executor.readLines()
	#	for line in lines:
	#		if len (line) > 0:
	#			print "OUT: " + line
	#executor.wait()
	
	stdinQueue.put ("/time")
	while executor.isRunning() or not stdoutQueue.empty():
		line = stdoutQueue.get (True)
		#print repr (line)
		#if len (line) > 0:
		print "OUT: " + line


if __name__ == "__main__":
	main (sys.argv)
