import lxml
from lxml_helpers.helpers import xml_namespace

class Unit(object):
	"""Defines a unit type"""

	def __init__(self, idx, measure):
		self.id = idx
		self.measure = measure

	def serialize(self, maker):
		with xml_namespace(maker, 'xbrli'):
			return maker.unit(
				maker.measure(self.measure),
				id = self.id
			)

def make_unit(data):
	#use data to derive id and measure for the unit
	return None