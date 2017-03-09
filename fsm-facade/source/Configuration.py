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
	
	def getBinPath (self):
		return self.binPath
	
	def getBinArgs (self):
		return self.binArgs
