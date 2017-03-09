import time
import subprocess
import select

class ProcessExecutor:
	def __init__ (self, binPath):
		self.binPath = binPath
	
	def start (self):
		print "Executing..."
		try:
			proc = subprocess.Popen (
[self.binPath, "--server-settings", "../../../factorio/dedicated/server-settings.json", "--start-server", "../../../factorio/dedicated/save.zip"],
stdin=subprocess.PIPE,
stdout=subprocess.PIPE)
			self.proc = proc
			self.stdout = proc.stdout
			self.stdin = proc.stdin
			#while proc.poll() is None:
			#	proc.stdin.write ("/quit\n")
		except OSError as ex:
			print "Error executing binary"
			print repr (ex)
		print "Process has been started"
	
	def writeLine (self, text):
		self.stdin.write (text + "\n")
	
	def readLines (self):
		output = []
		
		while True:
			inputdata, outputdata, exceptions = select.select ([self.stdout], [], [self.stdout], 0)
			if self.stdout in inputdata:
				line = self.stdout.readline()
				output.append (line.rstrip())
			if self.stdout in exceptions:
				print "EXCEPTION"
				break;
			else:
				break
		
		return output
	
	def wait (self):
		self.proc.wait()
	
	def isRunning (self):
		if self.proc.poll() is None:
			return True
		else:
			return False