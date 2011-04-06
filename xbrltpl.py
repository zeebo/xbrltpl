class Unit(object):
	"""Defines a unit type"""
	pass

class BaseFact(object):
	pass

class Fact(BaseFact):
	"""Defines a fact row for the template"""
	pass

class CalculationFact(BaseFact):
	"""Defines a calculation fact which is derived data from other facts"""
	pass

class Context(object):
	"""Context (date) for facts (instant or range)"""
	pass

class Matrix(object):
	"""Creates a 2d matrix that has operations to remove rows
		columns and grow/shrink without having to worry about it"""
	
	def __init__(self, default=None):
		self._data = [[]]
		self.default = default
	
	def __getitem__(self, index):
		row, col = index
		try:
			return self._data[row][col]
		except IndexError:
			return self.default
	
	def __setitem__(self, index, data):
		row, col = index
		try:
			self._data[row][col] = data
		except IndexError:
			self._assert_rows(row)
			self._assert_cols(col, row=row)
			self[row, col] = data
	
	def __delitem__(self, index):
		#First determine if we're deleting a single index, a row, or a column
		#deleting a column is worst perfoming.
		row, col = index
		if row is None:
			#Delete a column
			for row_value in (r for r in self._data if len(r) > col):
				del row_value[col]
		elif col is None:
			#Delete a row
			try:
				del self._data[row]
			except IndexError:
				pass
		else:
			#delete the row and column
			del self[row, None]
			del self[None, col]

	def _assert_rows(self, row):
		if len(self._data) <= row:
			rows_to_add = row - len(self._data) + 1
			for _ in xrange(rows_to_add):
				self._data.append([])
	
	def _assert_cols(self, col, row=0):
		self._assert_rows(row)
		column = self._data[row]
		if len(column) <= col:
			cols_to_add = col - len(column) + 1
			for _ in xrange(cols_to_add):
				column.append(self.default)

class Template(object):
	"""Template object. Defines structure of facts/units/contexts and
		serializes data into xml format"""
	def __init__(self, data = None):
		if data is not None:
			import pickle
			new_template = pickle.loads(data)
			self.__dict__.update(new_template.__dict__)
			self._data = Matrix()
			return
		
		self._contexts = []
		self._facts = []
		self._data = Matrix()
	
	def pickle(self):
		import pickle
		from contextlib import contextmanager

		@contextmanager
		def no_data_context():
			data_backup = self._data
			del self._data
			yield
			self._data = data_backup
		
		with no_data_context():
			return pickle.dumps(self)
	
	@property
	def contexts(self):
		return self._contexts
	
	@property
	def facts(self):
		return self._facts
	
	@property
	def units(self):
		return list(set(unit for fact, unit in self._facts))
	
	@property
	def data(self):
		temp_data = []
		for row_idx, (fact, unit) in enumerate(self._facts):
			temp_row = []
			for col_idx, context in enumerate(self._contexts):
				temp_row.append(self._data[row_idx, col_idx])
			temp_data.append(temp_row)
		return temp_data
	
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
	
	def get_cell_info(self, row, col):
		return self.facts[row], self.facts[col]
	
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
	
	def add_fact(self, fact, unit):
		if isinstance(fact, Fact) and isinstance(unit, Unit):
			self._facts.append( (fact, unit) )
		else:
			raise ValueError("Not passed fact/unit pair")
	
	def add_context(self, context):
		if isinstance(context, Context):
			self._contexts.append(context)
		else:
			raise ValueError("Not passed a context")
	
	def insert_fact(self, idx, fact, unit):
		if isinstance(fact, Fact) and isinstance(unit, Unit):
			self._facts.insert(idx, (fact, unit))
		else:
			raise ValueError("Not passed fact/unit pair")
	
	def insert_context(self, idx, context):
		if isinstance(context, Context):
			self._contexts.append(context)
		else:
			raise ValueError("Not passed a context")
	
	def del_fact(self, index):
		row = index
		try:
			row = self._facts.index(index)
		except ValueError:
			pass
		
		del self._facts[row]
		del self._data[row, None]
	
	def del_context(self, index):
		col = index
		try:
			col = self._contexts.index(index)
		except ValueError:
			pass
		
		del self._contexts[col]
		del self._data[None, col]

