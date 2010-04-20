class Controller(Object):
	def __init__(self):
		loadConfig("config")
		self.board = GameBoard(self.width, self.height)
		

	def loadConfig(self, filename):
		print "Loading game configuration..."
		config = ConfigParser.ConfigParser()
		config.read(filename)

		self.maxlength = int(config.get("GameBoard", "MaxLength"))
		self.width = int(config.get("GameBoard", "Width"))
		self.height = int(config.get("GameBoard", "Height"))
		
		self.minvisibility = int(config.get("Player", "MinVisibility"))
		self.maxvisibility = int(config.get("Player", "MaxVisibility"))

		print " Max Game Length:", self.maxlength
		print " Min Visibility:", self.minvisibility
		print " Max Visibility:", self.maxvisibility
		print " Game Height:", self.height
		print " Game Width:", self.width