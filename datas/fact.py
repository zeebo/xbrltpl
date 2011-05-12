import lxml
from lxml_helpers.helpers import xml_namespace
import random

class BaseFact(object):
	@property
	def label(self):
		if (hasattr(self, 'cache')):
			return self.cache
		self.cache = "{0:x}".format(random.getrandbits(60))
		return self.cache

	def serialize(self, value, unit, context, maker):
		return maker.fact('{0}'.format(value), **{
			'contextRef': context.make_id(),
			'unitRef': unit.id,
		})
	
	def make_loc(self, maker):
		with xml_namespace(maker, None, auto_convert=True) as maker:
			return maker.loc(**{
				'xlink:type': 'locator',
				'xlink:href': 'STUB',
				'xlink:label': self.label,
				'xlink:title': 'STUB TITLE',
			})
	
	def make_presentation(self, parent, order, maker):
		with xml_namespace(maker, None, auto_convert=True) as maker:
			return maker.presentationArc(**{
				'xlink:type': 'arc',
				'xlink:arcrole': 'STUB ARCROLE',
				'xlink:from': parent.label,
				'xlink:to': self.label,
				'xlink:title': 'presentation: {0} to {1}'.format(
						parent.label, self.label
					),
				'use': 'optional',
				'order': '{0:.1f}'.format(order)
			})

class Fact(BaseFact):
	"""Defines a fact row for the template"""
	pass

class CalculationFact(BaseFact):
	"""Defines a calculation fact which is derived data from other facts"""
	pass


