from base import TestCase
from datas.fact import Fact

class FactTest(TestCase):
	def test_label_cache(self):
		new_fact = Fact()
		self.assertEqual(new_fact.label, new_fact.label)