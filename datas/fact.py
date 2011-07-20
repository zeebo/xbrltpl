import lxml
from lxml_helpers.helpers import xml_namespace
from helpers import uid

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

class Fact(object):
	def __init__(self, with_calc=None, **kwargs):
		self._cache = {}
		self._cache.update(kwargs)
		self.calc_items = with_calc
	
	def __repr__(self):
		return 'Fact[{0}]'.format(self.id)
	
	@cached_property
	def namespace(self):
		return 'us-gaap'

	@cached_property
	def id(self):
		return uid()

	@cached_property
	def label(self):
		return uid()
	
	@cached_property
	def label_text(self):
		return uid()
	
	@cached_property
	def href(self):
		return uid()
	
	@cached_property
	def title(self):
		return uid()

	@cached_property
	def period(self):
		return 'duration'
		
	def serialize(self, value, unit, context, maker):
		with xml_namespace(maker, self.namespace) as maker:
			return maker.__getattr__(self.label)(
				'{0}'.format(value),
				**{
					'contextRef': context.make_id(),
					'unitRef': unit.id,
					'decimals': '0',
				}
			)
	
	@property
	def is_calc(self):
		return self.calc_items is not None


