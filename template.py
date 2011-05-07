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
		self._tree = {}
	
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
	
	def walk_facts(self):
		for child in self._facts:
			yield (self.find_parent(child), child)
	
	def find_parent(self, child):
		return self._tree[child]
	
	def find_children(self, parent):
		children = []
		for child in self._tree:
			if self.find_parent(child) == parent:
				children.append(child)
		return children

	def add_relationship(self, parent, child):
		self._tree[child] = parent
	
	def del_relationship(self, child):
		parent = self.find_parent(child)
		for some_child in self.find_children(child):
			self.add_relationship(parent, some_child)
		del self._tree[child]
	
	def add_fact(self, fact, unit, parent=None):
		assert isinstance(fact, BaseFact)
		assert isinstance(unit, Unit)
		self._facts.append( (fact, unit) )
		self.add_relationship(parent, (fact, unit) )
	
	def add_context(self, context):
		assert isinstance(context, Context)
		self._contexts.append(context)
	
	def insert_fact(self, idx, fact, unit, parent=None):
		assert isinstance(fact, BaseFact)
		assert isinstance(unit, Unit)
		self._facts.insert(idx, (fact, unit))
		self.add_relationship(parent, (fact, unit) )
	
	def insert_context(self, idx, context):
		assert isinstance(context, Context)
		self._contexts.insert(idx, context)
	
	def del_fact(self, index):
		try:
			index = self._facts.index(index)
		except ValueError:
			pass
		
		self.del_relationship(self._facts[index])
		del self._facts[index]
	
	def del_context(self, index):
		try:
			index = self._contexts.index(index)
		except ValueError:
			pass
		
		del self._contexts[index]