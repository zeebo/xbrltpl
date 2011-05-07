import lxml

class BaseFact(object):
	pass

class Fact(BaseFact):
	"""Defines a fact row for the template"""
	def serialize(self, value, unit, context, maker):
		return maker.fact('{0}'.format(value), **{
			'contextRef': context.make_id(),
			'unitRef': unit.id,
		})

class CalculationFact(BaseFact):
	"""Defines a calculation fact which is derived data from other facts"""
	def serialize(self, value, unit, context, maker):
		return maker.fact('{0}'.format(value), **{
			'contextRef': context.make_id(),
			'unitRef': unit.id,
		})

