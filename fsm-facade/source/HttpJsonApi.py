import threading
import BaseHTTPServer
import urlparse


class GetHandler (BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(self):
		
		cmdMap = {
				"/start" : self.doStart,
				"/stop" : self.doStop,
				"/quit" : self.doQuit,
				"/chat/send" : self.doChatSend
				}
		
		parsed_path = urlparse.urlparse(self.path)
		self.send_response (200)
		self.end_headers()
		self.wfile.write ("<html>\
<title>Wooo! Clicky things!</title>\
<body>\
<form action=\"/chat/send\" method=\"get\">\
Send server chat message:<br />\
<input type=\"text\" name=\"text\" /><br />\
<input type=\"submit\" value=\" Send! \" />\
</form>\
<a href=\"/start\">Start Factorio server</a><br />\
<a href=\"/stop\">Stop Factorio server</a><br />\
<a href=\"/quit\">Quit fsm-facade!</a><br />\
</body>\
</html>")
		
		cmd = parsed_path.path
		print "cmd is %s" % cmd
		if cmd in cmdMap:
			cmdMap[cmd](parsed_path)
	
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

class HttpJsonApi:# (threading.Thread):
	def __init__ (self, api, address, port):
		GetHandler.api = api
		self.server = BaseHTTPServer.HTTPServer ((address, port), GetHandler)
	
	def start (self):
		thread = threading.Thread (target=self.server.serve_forever)
		thread.start()
	
	def stop (self):
		self.server.server_close()
		self.server.shutdown()
