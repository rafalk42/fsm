import ConfigParser

class ConfigurationException(Exception):
	pass

class Configuration:
	def __init__(self, configPath):
		config = ConfigParser.RawConfigParser()
		loaded = config.read(configPath)
		
		if len (loaded) == 0:
			raise ConfigurationException("couldn't read configuration file at: " + configPath)
		
		self.binPath = config.get ("main", "binPath")
		binArgs = config.get ("main", "binArgs")
		self.binArgs = binArgs.split (" ")
		
		self.webAddress = config.get ("web", "address")
		self.webPort = int (config.get ("web", "port"))
		self.webStaticFilesRootPath = config.get ("web", "staticFilesRootPath")
	
	def getBinPath (self):
		return self.binPath
	
	def getBinArgs (self):
		return self.binArgs
	
	def getWebAddress (self):
		return self.webAddress
	
	def getWebPort (self):
		return self.webPort
	
	def getWebStaticFilesRootPath (self):
		return self.webStaticFilesRootPath
