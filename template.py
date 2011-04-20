from datas.fact import BaseFact
from datas.context import Context
from datas.unit import Unit

class Template(object):
	"""Template object. Defines structure of facts/units/contexts and
		serializes data into xml format"""
	def __init__(self, data = None):
		if data is not None:
			import pickle
			new_template = pickle.loads(data)
			self.__dict__.update(new_template.__dict__)
			return
		
		self._contexts = []
		self._facts = []
	
	def pickle(self):
		import pickle
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
	
	def get_cell_info(self, row, col):
		return self.facts[row], self.facts[col]
	
	def add_fact(self, fact, unit):
		assert isinstance(fact, BaseFact)
		assert isinstance(unit, Unit)
		self._facts.append( (fact, unit) )
	
	def add_context(self, context):
		assert isinstance(context, Context)
		self._contexts.append(context)
	
	def insert_fact(self, idx, fact, unit):
		assert isinstance(fact, BaseFact)
		assert isinstance(unit, Unit)
		self._facts.insert(idx, (fact, unit))
	
	def insert_context(self, idx, context):
		assert isinstance(context, Context)
		self._contexts.insert(idx, context)
	
	def del_fact(self, index):
		row = index
		try:
			row = self._facts.index(index)
		except ValueError:
			pass
		
		del self._facts[row]
	
	def del_context(self, index):
		col = index
		try:
			col = self._contexts.index(index)
		except ValueError:
			pass
		
		del self._contexts[col]