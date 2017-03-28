import threading
import BaseHTTPServer
import urlparse
import socket
import os


class GetHandler (BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(self):
		
		cmdMap = {
				"/start" : self.doStart,
				"/stop" : self.doStop,
				"/quit" : self.doQuit,
				"/chat/send" : self.doChatSend
				}
		
		parsed_path = urlparse.urlparse(self.path)
		qs = urlparse.parse_qs (parsed_path.query)
		if parsed_path.path is "/":
			print ("No path, serving index.html")
			path_chunks = ["index.html"]
		else:
			path_chunks = parsed_path.path.split("/")
			if len (path_chunks[0]) is 0:
				path_chunks = path_chunks[1:]
		
		print (path_chunks)
		print (qs)
		
		
		if path_chunks[0] is "api": # handle api
			command = path_chunks[1]
		else: # handle static files
			filePath = os.path.join (self.staticFilePath, *path_chunks)
			print ("Will server file: \"%s\"" % filePath)
			if not os.path.isfile (filePath):
				self.send_response (404)
				self.end_headers()
				self.wfile.write ("404 - not found")
			else:
				fileHandle = open (filePath, "r")
				self.send_response (200)
				self.end_headers()
				self.wfile.write (fileHandle.read())
		
#		cmd = parsed_path.path
#		print "cmd is %s" % cmd
#		if cmd in cmdMap:
#			cmdMap[cmd](parsed_path)
	
	def doStart (self, path):
		self.api.serverStart()
	
	def doStop (self, path):
		self.api.serverStop()
	
	def doQuit (self, path):
		self.api.quit()
	
	def doChatSend (self, path):
		params = urlparse.parse_qs (path.query)
		message = params["text"][0]
		print repr (message)
		self.api.chatSend (message)

class HTTPServerV6 (BaseHTTPServer.HTTPServer):
	address_family = socket.AF_INET6

class HttpServer:# (threading.Thread):
	def __init__ (self, api, address, port, staticFilePath):
		GetHandler.api = api
		GetHandler.staticFilePath = staticFilePath
		self.server = HTTPServerV6 ((address, port), GetHandler)
	
	def start (self):
		thread = threading.Thread (target=self.server.serve_forever)
		thread.start()
	
	def stop (self):
		self.server.server_close()
		self.server.shutdown()
