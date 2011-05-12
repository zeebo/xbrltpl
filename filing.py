from template import Template
from datas.matrix import Matrix
import datetime
#Filing object contains _ALL_ the data for a specific filing.

class Filing(object):
	"""Filing class holds a collection of charts and company/date"""

	def __init__(self, with_charts=None, with_date=None, with_company=None):
		if with_charts is not None:
			self.charts = with_charts[:] #store a copy
		else:
			self.charts = []
		
		if with_date is not None:
			self.date = with_date
		else:
			self.date = datetime.date.today()
		
		if with_company is not None:
			self.company = with_company
		else:
			#might replace this to be a model somehow
			class Company(object):
				pass
			self.company = Company
	
	#Convenience methods for getting all the data out of the charts
	@property
	def contexts(self):
		for c in self.charts:
			for context in c.contexts:
				yield context
	
	@property
	def units(self):
		for c in self.charts:
			for unit in c.units:
				yield unit
	
	@property
	def data_stream(self):
		for c in self.charts:
			for data in c.data_stream:
				yield data