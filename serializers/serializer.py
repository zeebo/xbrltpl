from filing import Filing

#Serializer determines which files need to be serialized and dispatches
#to the appropriate objects that serialize that type of file with a
#specific Filing object

class Serializer(object):
	def __init__(self, filing):
		assert isinstance(filing, Filing)
		self.filing = filing
	
	