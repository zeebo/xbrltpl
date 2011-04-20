from base import TestCase
from lxml_helpers.helpers import xml_namespace

class HelpersTest(TestCase):
	def test_xml_namespace(self):
		from lxml.builder import ElementMaker
		maker = ElementMaker(namespace='too', nsmap ={'bar':'bar', 'foo':'too'})
		self.assertEqual(maker._namespace, '{too}')
		with xml_namespace(maker, 'bar'):
			self.assertEqual(maker._namespace, '{bar}')
		self.assertEqual(maker._namespace, '{too}')