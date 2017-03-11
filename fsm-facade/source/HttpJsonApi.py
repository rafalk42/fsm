import threading
import BaseHTTPServer
import urlparse


class GetHandler (BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(self):
		
		cmdMap = {
				"/start" : self.doStart,
				"/stop" : self.doStop,
				"/quit" : self.doQuit
				}
		
		parsed_path = urlparse.urlparse(self.path)
		self.send_response (200)
		self.end_headers()
		self.wfile.write ("<html>\
<title>Wooo! Clicky things!</title>\
<body>\
<a href=\"/start\">Start Factorio server</a><br />\
<a href=\"/stop\">Stop Factorio server</a><br />\
<a href=\"/quit\">Quit fsm-facade!</a><br />\
</body>\
</html>")
		
		cmd = parsed_path.path
		print "cmd is %s" % cmd
		if cmd in cmdMap:
			cmdMap[cmd]()
	
	def doStart (self):
		self.api.serverStart()
	
	def doStop (self):
		self.api.serverStop()
	
	def doQuit (self):
		self.api.quit()

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
