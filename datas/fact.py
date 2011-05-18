import lxml
from lxml_helpers.helpers import xml_namespace
import random

def cached_property(function):
	@property
	def new_func(self):
		try:
			return self._cache[function.func_name]
		except:
			if (not hasattr(self, '_cache')):
				self._cache = {}
			
			self._cache[function.func_name] = function(self)
			return self._cache[function.func_name]
	return new_func

class BaseFact(object):
	def __init__(self, **kwargs):
		self._cache = {}
		self._cache.update(kwargs)

	@cached_property
	def label(self):
		return "{0:x}".format(random.getrandbits(60))
	
	@cached_property
	def label_text(self):
		return "{0:x}".format(random.getrandbits(60))
	
	@cached_property
	def href(self):
		return "{0:x}".format(random.getrandbits(60))
	
	@cached_property
	def title(self):
		return "{0:x}".format(random.getrandbits(60))
		
	def serialize(self, value, unit, context, maker):
		return maker.fact('{0}'.format(value), **{
			'contextRef': context.make_id(),
			'unitRef': unit.id,
		})
	
class Fact(BaseFact):
	"""Defines a fact row for the template"""
	pass

class CalculationFact(BaseFact):
	"""Defines a calculation fact which is derived data from other facts"""
	pass


