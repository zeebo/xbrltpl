import lxml

class BaseFact(object):
	pass

class Fact(BaseFact):
	"""Defines a fact row for the template"""
	def serialize(self, value, maker):
		return maker.fact('{}'.format(value))

class CalculationFact(BaseFact):
	"""Defines a calculation fact which is derived data from other facts"""
	def serialize(self, value, maker):
		return maker.fact('{}'.format(value))

