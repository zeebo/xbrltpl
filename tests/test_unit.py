from base import TestCase
from datas.unit import Unit

class ContextTest(TestCase):
	def test_init(self):
		unit = Unit('Shares', 'xbrli:shares')
	
	def test_serialize(self):
		from lxml.builder import ElementMaker
		nsmap = {
			'xbrli': 'http://some.url.com/',
			'test': 'http://test.com/',
		}
		maker = ElementMaker(namespace='http://test.com/', nsmap=nsmap)
		unit = Unit('Shares', 'xbrli:shares')
		self.assertEqual(maker._namespace,'{http://test.com/}')
		tree = unit.serialize(maker)

		from lxml import etree
		string = etree.tostring(tree)
		self.assertEqual(string, '<xbrli:unit xmlns:test="http://test.com/" xmlns:xbrli="http://some.url.com/" id="Shares"><xbrli:measure>xbrli:shares</xbrli:measure></xbrli:unit>')
		self.assertEqual(maker._namespace,'{http://test.com/}')