from datas.fact import BaseFact
from datas.context import Context
from datas.unit import Unit
from collections import defaultdict

class Template(object):
	"""Template object. Defines structure of facts/units/contexts and
		serializes data into xml format"""
	def __init__(self):
		self._contexts = []
		self._tree = defaultdict(list)
	
	@property
	def contexts(self):
		return self._contexts
	
	@property
	def facts(self):
		facts = []
		for parent, children in self._tree.items():
			facts.extend(fact for fact, _ in children)
		return facts
	
	@property
	def units(self):
		units = []
		for parent, children in self._tree.items():
			units.extend(unit for _, unit in children)
		return units
	
	@property
	def rows(self):
		return zip(self.facts, self.units)
	
	@property
	def tree(self):
		return self._tree
	
	def walk_tree(self):
		return [(self.find_parent(item), item) for item in self.rows]
	
	def ordered_yield(self, root=None):
		for child in self._tree[root]:
			yield child
			if child in self._tree:
				for i in self.ordered_yield(root=child):
					yield i
	
	def ordered_tree(self):
		return list(self.ordered_yield())
	
	def get_index(self, child):
		return list(self.ordered_yield()).index(child)
	
	def find_parent(self, child):
		for parent, children in self._tree.items():
			if child in children:
				return parent
	
	def find_children(self, parent):
		return self._tree[parent]
	
	def add_fact(self, fact, unit, parent=None):
		assert isinstance(fact, BaseFact)
		assert isinstance(unit, Unit)
		self._tree[parent].append((fact, unit))
	
	def insert_fact(self, idx, fact, unit, parent=None):
		assert isinstance(fact, BaseFact)
		assert isinstance(unit, Unit)
		self._tree[parent].insert(idx, (fact, unit))
	
	def del_fact(self, fact, unit):
		child = fact, unit
		#Move children to it's parent
		parent = self.find_parent(child)
		children = self.find_children(child)
		self._tree[parent].extend(self.find_children(child))
		self._tree[parent].remove(child)
		if parent is not None and child in self._tree:
			del self._tree[child]
	
	#Context related functions
	def add_context(self, context):
		assert isinstance(context, Context)
		self._contexts.append(context)
	
	def insert_context(self, idx, context):
		assert isinstance(context, Context)
		self._contexts.insert(idx, context)
	
	def del_context(self, index):
		try:
			index = self._contexts.index(index)
		except ValueError:
			pass
		
		del self._contexts[index]
