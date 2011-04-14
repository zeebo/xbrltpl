from template import Template
from datas.matrix import Matrix

#Filing object contains _ALL_ the data for a specific filing.

class Filing(object):
	"""Filing class holds a template and data to go in it"""

	def __init__(self, with_template=None, with_data=None):
		if with_template is not None:
			self._template = with_template
		else:
			self._template = Template()
		
		if with_data is not None:
			self._data = with_data
		else:
			self._data = Matrix()
	
	def pickle(self):
		import pickle
		return pickle.dumps(self)
	
	@property
	def data(self):
		temp_data = []
		for row_idx, (fact, unit) in enumerate(self._facts):
			temp_row = []
			for col_idx, context in enumerate(self._contexts):
				temp_row.append(self._data[row_idx, col_idx])
			temp_data.append(temp_row)
		return temp_data
	
	@property
	def contexts(self):
		return self._template.contexts
	
	@property
	def facts(self):
		return self._template.facts
	
	@property
	def units(self):
		return list(set(unit for fact, unit in self._template.facts))
	
	def pretty_data(self):
		return '\n'.join(
			'\t'.join(
				item is None and '-' or item.__repr__() for item in row
			)
			for row in self.data
		)
	
	def get_row_col(self, fact, unit, context):
		row = self._facts.index((fact, unit))
		col = self._contexts.index(context)
		return (row, col)
	
	def _transform_index(self, index):
		if not isinstance(index, tuple):
			raise KeyError('Invalid key')
		row, col = index
		if isinstance(row, tuple):
			#We have a get based on things
			row, col = self.get_row_col(row[0], row[1], col)
		return row, col
	
	def __getitem__(self, index):
		row, col = self._transform_index(index)
		return self._data[row, col]
	
	def __setitem__(self, index, data):
		row, col = self._transform_index(index)
		#TODO: validation
		#(fact, unit), context = self.get_cell_info(row, col)
		#fact.validate(data), unit.validate(data), context.validate(data)
		
		self._data[row, col] = data
	
	def __delitem__(self, index):
		row, col = self._transform_index(index)
		self._data[row, col] = self._data.default
	
	def del_fact(self, index):
		row = index
		try:
			row = self._template._facts.index(index)
		except ValueError:
			pass
		self._template.del_fact(row)
		del self._data[row, None]

	def del_context(self, index):
		col = index
		try:
			col = self._template._contexts.index(index)
		except ValueError:
			pass
		self._template.del_context(col)
		del self._data[None, row]