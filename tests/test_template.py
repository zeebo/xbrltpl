from base import TestCase
from template import Template
from datas.fact import Fact
from datas.context import Context
from datas.unit import Unit
from mock import Mock

import pickle

def m(name, spec):
	mock = Mock(name=name, spec=spec)
	mock.__repr__ = lambda x: name
	return mock

class TemplateTest(TestCase):
	def setUp(self):
		self.t = Template()
		
		self.tree = Template()
		a,b,c,d,e,f,g = self.get_some_facts()
		self.tree.add_fact(*a)
		self.tree.add_fact(*b, parent=a)
		self.tree.add_fact(*c, parent=a)
		self.tree.add_fact(*d, parent=a)
		self.tree.add_fact(*e, parent=c)
		self.tree.add_fact(*f, parent=c)
		self.tree.add_fact(*g)
	
	def get_some_facts(self, cache={}):
		if len(cache):
			return (item for _, item in sorted(cache.items()))
		cache['a'] = m('facta', Fact), m('unita', Unit)
		cache['b'] = m('factb', Fact), m('unitb', Unit)
		cache['c'] = m('factc', Fact), m('unitc', Unit)
		cache['d'] = m('factd', Fact), m('unitd', Unit)
		cache['e'] = m('facte', Fact), m('unite', Unit)
		cache['f'] = m('factf', Fact), m('unitf', Unit)
		cache['g'] = m('factg', Fact), m('unitg', Unit)
		return self.get_some_facts()


	def test_context_methods(self):
		context =  m('context', Context)
		context2 =  m('context2', Context)
		self.assertEqual(self.t.contexts, [])
		self.t.add_context(context)
		self.assertEqual(self.t.contexts, [context])
		self.t.del_context(context)
		self.assertEqual(self.t.contexts, [])

		self.t.insert_context(0, context)
		self.t.insert_context(0, context2)
		self.assertEqual(self.t.contexts, [context2, context])

		self.t.del_context(0)
		self.assertEqual(self.t.contexts, [context])
	
	def test_fact_methods(self):
		fact, unit = m('fact', Fact), m('unit', Unit)
		self.assertEqual(self.t.facts, [])
		self.assertEqual(self.t.units, [])
		self.t.add_fact(fact, unit)
		self.assertEqual(self.t.facts, [fact])
		self.assertEqual(self.t.units, [unit])
		self.t.del_fact(fact, unit)
		self.assertEqual(self.t.facts, [])
		self.assertEqual(self.t.units, [])

	def test_find_parent(self):
		a = m('facta', Fact), m('unita', Unit)
		b = m('factb', Fact), m('unitb', Unit)

		self.t.add_fact(*a)
		self.t.add_fact(*b, parent=a)

		self.assertEqual(a, self.t.find_parent(b))
		self.assertEqual(None, self.t.find_parent(a))
	
	def test_tree_operations(self):
		# Bunch of fact/unit combos
		a,b,c,d,e,f,g = self.get_some_facts()
		self.assertEqual({None:[a,g], a:[b,c,d], c:[e,f]}, self.tree.tree)
		self.tree.del_fact(*c)
		self.assertEqual({None:[a,g], a:[b,d,e,f]}, self.tree.tree)
	
	def test_walk_tree(self):
		# Bunch of fact/unit combos
		a,b,c,d,e,f,g = self.get_some_facts()
		self.assertEqual(set([
			(None, a),
			(None, g),
			(a, b),
			(a, c),
			(a, d),
			(c, e),
			(c, f),
		]), set(self.tree.walk_tree()))
	
	def test_ordered_yield(self):
		a,b,c,d,e,f,g = self.get_some_facts()
		self.assertEqual(list(self.tree.ordered_yield()), [a,b,c,e,f,d,g])
	
	def test_get_index(self):
		a,b,c,d,e,f,g = self.get_some_facts()
		self.assertEqual(self.tree.get_index(d), 5)
	
	def test_insert_fact(self):
		a,b,c,d,e,f,g = self.get_some_facts()
		h = m('facth', Fact), m('unith', Unit)
		self.tree.insert_fact(1, *h)
		self.assertEqual(list(self.tree.ordered_yield()), [a,b,c,e,f,d,h,g])
