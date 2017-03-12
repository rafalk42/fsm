import threading


class ServerApi:
	def __init__ (self, server):
		self.server = server
		self.quitEvent = threading.Event()
	
	def isQuit (self):
		return self.quitEvent.is_set()
	
	def waitForQuit (self, timeout = None):
		ret = self.quitEvent.wait(timeout)
		
		if ret is True:
			return True
		else:
			return False
	
	def quit (self):
		self.server.serverStop()
		print "Quit called, settting quitEvent"
		self.quitEvent.set()
	
	def serverStart (self):
		self.server.serverStart()
	
	def serverStop (self):
		self.server.serverStop()
	
	def chatSend (self, text):
		self.server.chatSend (text)
