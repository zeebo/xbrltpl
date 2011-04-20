from base import TestCase
from lxml_helpers.helpers import xml_namespace, make_attrib, convert_attribs

class HelpersTest(TestCase):
	def setUp(self):
		self.nsmap = {
			'test': 'http://test/',
			'foo': 'http://foo/',
			'bar': 'http://bar/',
		}
	def test_xml_namespace(self):
		from lxml.builder import ElementMaker
		maker = ElementMaker(namespace='http://foo/', nsmap =self.nsmap)
		self.assertEqual(maker._namespace, '{http://foo/}')
		with xml_namespace(maker, 'bar'):
			self.assertEqual(maker._namespace, '{http://bar/}')
		self.assertEqual(maker._namespace, '{http://foo/}')
	def test_make_attrib(self):
		self.assertEqual('{http://test/}name', make_attrib('test:name', self.nsmap))
		self.assertEqual('{http://test/}name2', make_attrib('test:name2', self.nsmap))
		self.assertEqual('{http://foo/}name', make_attrib('foo:name', self.nsmap))
		self.assertEqual('{http://bar/}name', make_attrib('bar:name', self.nsmap))
	
	def test_convert_attribs(self):
		attribs = {
			'test:name1': 'data1',
			'foo:name2': 'data2',
			'bar:name3': 'data3',
		}

		self.assertEqual(convert_attribs(attribs, self.nsmap), {
			'{http://test/}name1': 'data1',
			'{http://foo/}name2': 'data2',
			'{http://bar/}name3': 'data3',
		})