import threading
import Queue


class ServerProcess:
	def __init__ (self, executor):
		self.executor = executor
		self.isRunning = False
	
	def serverStart (self):
		if self.isRunning:
			print "Factorio server is already running"
			return
		
		print "Starting Factorio server"
		
		if not self.executor.start():
			print "Failed to start process"
			return False
		
		self.stdoutQueue = self.executor.getStdoutQueue()
		self.stdinQueue = self.executor.getStdinQueue()
		
		self.stdoutProcessor = StdoutProcessor (self.stdoutQueue)
		self.stdoutProcessor.start()
		
		self.isRunning = True
	
	def serverStop (self):
		if not self.isRunning:
			print "Factorio server is not running"
			return
		
		print "Stopping Factorio server"
		
		print "Sending quit command"
		self.stdinQueue.put ("/quit")
		
		self.executor.wait()
		self.executor.stop()
		
		print "Stopping StdoutProcessor"
		self.stdoutProcessor.stop()
		print "Waiting for StdoutProcessor to quit"
		self.stdoutProcessor.join()
		
		print "All quit"
		
		self.isRunning = False
	
	def chatSend (self, text):
		if text[0] == "/":
			print "Refusing to send command: %s" % text
			return
		
		self.stdinQueue.put (text)

class StdoutProcessor (threading.Thread):
	def __init__ (self, queue):
		threading.Thread.__init__ (self)
		self.queue = queue
		self.exit = False
	
	def stop (self):
		self.exit = True
	
	def run (self):
		print "Started StdoutProcessor thread"
		
		while not self.exit:
			try:
				line = self.queue.get (True, 0.1)
				print "OUT: " + line
			except Queue.Empty:
				pass
		
		print "Finished StdoutProcessor thread"

