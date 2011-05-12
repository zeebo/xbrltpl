from base import TestCase
from datas.fact import BaseFact, Fact, CalculationFact

class FactTest(TestCase):
	def test_label_cache(self):
		for cls in (BaseFact, Fact, CalculationFact):
			new_fact = cls()
			self.assertEqual(new_fact.label, new_fact.label)