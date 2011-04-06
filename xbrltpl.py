class Unit(object):
	"""Defines a unit type"""
	pass

class BaseFact(object):
	pass

class Fact(BaseFact):
	"""Defines a fact row for the template"""
	pass

class CalculationFact(BaseFact):
	"""Defines a calculation fact which is derived data from other facts"""
	pass

class Context(object):
	"""Context (date) for facts (instant or range)"""
	pass

class Template(object):
	"""Template object. Defines structure of facts/units/contexts and
		serializes data into xml format"""
	pass