from template import Template
from datas.matrix import Matrix
#Chart object contains the data for a specific chart.

class Chart(object):
	"""Chart class holds a template and data to go in it"""

	def __init__(self, with_template=None, with_data=None):
		if with_template is not None:
			self._template = with_template
		else:
			self._template = Template()
		
		self._data = {}

	def pickle(self):
		import pickle
		return pickle.dumps(self)
	
	@property
	def data_stream(self):
		"""Yields tuples:
			(fact, unit), context data"""
		for index in self._template.rows:
			for context in self._template.contexts:
				yield (index, context, self._data[(index, context)])
	
	@property
	def contexts(self):
		return self._template.contexts
	
	@property
	def facts(self):
		return self._template.facts
	
	@property
	def units(self):
		return self._template.units
	
	def __getitem__(self, index):
		return self._data[index]
	
	def __setitem__(self, index, data):
		self._data[index] = data
	
	def __delitem__(self, index):
		self._data[index] = None