import time
import subprocess
import select
import threading
import Queue


class ProcessExecutor:
	def __init__ (self, binPath, binArgs):
		self.binPath = binPath
		self.binArgs = binArgs
	
	def start (self):
		print "Executing " + self.binPath + "..."
		try:
			proc = subprocess.Popen ([self.binPath] + self.binArgs, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
			
			self.stdoutLinesQueue = Queue.Queue()
			self.stdinLinesQueue = Queue.Queue()
			self.readerThread = ProcessStdoutReader (proc.stdout, self.stdoutLinesQueue)
			self.readerThread.start()
			
			self.writerThread = ProcessStdinWriter (proc.stdin, self.stdinLinesQueue)
			self.writerThread.start()
			
			self.proc = proc
			self.stdout = proc.stdout
			self.stdin = proc.stdin
		except OSError as ex:
			print "Error executing binary"
			print repr (ex)
		print "Process has been started"
	
	def getStdoutQueue (self):
		return self.stdoutLinesQueue
	
	def getStdinQueue (self):
		return self.stdinLinesQueue
	
	def wait (self):
		self.proc.wait()
		
		print "Notifying threads to stop"
		self.readerThread.stop()
		self.writerThread.stop()
		
		print "Waiting for threads to end"
		self.readerThread.join()
		self.writerThread.join()
		print "All threads clear"
	
	def isRunning (self):
		if self.proc.poll() is None:
			return True
		else:
			return False

class ProcessStdoutReader (threading.Thread):
	def __init__ (self, stdout, queue):
		threading.Thread.__init__ (self)
		self.stdout = stdout
		self.queue = queue
		self.exit = False
	
	def run (self):
		print "ProcessStdoutReader started"
		
		while not self.exit:
			try:
				inputdata, outputdata, exceptions = select.select ([self.stdout], [], [self.stdout], 0.1)
			except select.error, v:
				if v[0] != errno.EINTR:
					print "EINTR"
					raise
				else:
					print repr (v)
					break
			if self.stdout in inputdata:
				line = self.stdout.readline()
				lineStripped = line.rstrip()
				if len (lineStripped) > 0:
					self.queue.put (lineStripped)
			if self.stdout in exceptions:
				print "EXCEPTION"
				break;
		
		print "ProcessStdoutReader finished"
	
	def stop (self):
		self.exit = True

class ProcessStdinWriter (threading.Thread):
	def __init__ (self, stdin, queue):
		threading.Thread.__init__ (self)
		self.stdin = stdin
		self.queue = queue
		self.exit = False
	
	def run (self):
		print "ProcessStdinWriter started"
		
		while not self.exit:
			try:
				line = self.queue.get (True, 0.1)
				self.stdin.write (line + "\n")
			except Queue.Empty:
				pass
		
		print "ProcessStdoutWriter finished"
	
	def stop (self):
		self.exit = True
