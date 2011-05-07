from base import TestCase
from template import Template
from datas.fact import BaseFact
from datas.context import Context
from datas.unit import Unit
from mock import Mock

import pickle

def m(name, spec):
	return Mock(name=name, spec=spec)

class TemplateTest(TestCase):
	def setUp(self):
		self.t = Template()
	
	def test_context_methods(self):
		context =  m('context', Context)
		self.assertEqual(self.t.contexts, [])
		self.t.add_context(context)
		self.assertEqual(self.t.contexts, [context])
		self.t.del_context(context)
		self.assertEqual(self.t.contexts, [])
	
	def test_fact_methods(self):
		fact, unit = m('fact', BaseFact), m('unit', Unit)
		self.assertEqual(self.t.facts, [])
		self.assertEqual(self.t.units, [])
		self.t.add_fact(fact, unit)
		self.assertEqual(self.t.facts, [(fact, unit)])
		self.assertEqual(self.t.units, [unit])
		self.t.del_fact((fact, unit))
		self.assertEqual(self.t.facts, [])
		self.assertEqual(self.t.units, [])

	def test_tree_additions(self):
		# Bunch of fact/unit combos
		a = m('facta', BaseFact), m('unita', Unit)
		b = m('factb', BaseFact), m('unitb', Unit)
		c = m('factc', BaseFact), m('unitc', Unit)
		d = m('factd', BaseFact), m('unitd', Unit)
		e = m('facte', BaseFact), m('unite', Unit)
		f = m('factf', BaseFact), m('unitf', Unit)
		g = m('factg', BaseFact), m('unitg', Unit)

		self.t.add_fact(*a)
		self.t.add_fact(*b, parent=a)
		self.t.add_fact(*c, parent=a)
		self.t.add_fact(*d, parent=a)
		self.t.add_fact(*e, parent=c)
		self.t.add_fact(*f, parent=c)
		self.t.add_fact(*g)

		self.assertEqual({a:None, b:a, c:a, d:a, e:c, f:c, g:None}, self.t._tree)
	
	def test_find_parent(self):
		a = m('facta', BaseFact), m('unita', Unit)
		b = m('factb', BaseFact), m('unitb', Unit)

		self.t.add_fact(*a)
		self.t.add_fact(*b, parent=a)

		self.assertEqual(a, self.t.find_parent(b))
		self.assertEqual(None, self.t.find_parent(a))
	
	def test_tree_deletions(self):
		# Bunch of fact/unit combos
		a = m('facta', BaseFact), m('unita', Unit)
		b = m('factb', BaseFact), m('unitb', Unit)
		c = m('factc', BaseFact), m('unitc', Unit)
		d = m('factd', BaseFact), m('unitd', Unit)
		e = m('facte', BaseFact), m('unite', Unit)
		f = m('factf', BaseFact), m('unitf', Unit)
		g = m('factg', BaseFact), m('unitg', Unit)

		self.t.add_fact(*a)
		self.t.add_fact(*b, parent=a)
		self.t.add_fact(*c, parent=a)
		self.t.add_fact(*d, parent=a)
		self.t.add_fact(*e, parent=c)
		self.t.add_fact(*f, parent=c)
		self.t.add_fact(*g)
		
		self.t.del_fact(c)

		self.assertEqual({a:None, b:a, d:a, e:a, f:a, g:None}, self.t._tree)
	
	def test_walk_facts(self):
		# Bunch of fact/unit combos
		a = m('facta', BaseFact), m('unita', Unit)
		b = m('factb', BaseFact), m('unitb', Unit)
		c = m('factc', BaseFact), m('unitc', Unit)
		d = m('factd', BaseFact), m('unitd', Unit)
		e = m('facte', BaseFact), m('unite', Unit)
		f = m('factf', BaseFact), m('unitf', Unit)
		g = m('factg', BaseFact), m('unitg', Unit)

		self.t.add_fact(*a)
		self.t.add_fact(*b, parent=a)
		self.t.add_fact(*c, parent=a)
		self.t.add_fact(*d, parent=a)
		self.t.add_fact(*e, parent=c)
		self.t.add_fact(*f, parent=c)
		self.t.add_fact(*g)

		self.assertEqual(set([
			(None, a),
			(None, g),
			(a, b),
			(a, c),
			(a, d),
			(c, e),
			(c, f),
		]), set(self.t.walk_facts()))
