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
