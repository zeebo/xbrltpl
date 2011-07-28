import lxml
from lxml_helpers.helpers import xml_namespace

class Context(object):
	"""Context (date) for facts (instant or range)"""
	def __init__(self, instant, dates):
		self.instant = instant
		self.date_strings = dates
	
	def serialize(self, maker, cik):
		with xml_namespace(maker, 'xbrli'):
			return maker.context(
				maker.entity(
					maker.identifier('%010d' % int(cik),
					scheme="http://www.sec.gov/CIK")
				),
				maker.period(
					*self.period_node(maker)
				),
				id = self.make_id()
			)
	
	def period_node(self, maker):
		with xml_namespace(maker, 'xbrli'):
			if self.instant:
				return [maker.instant(self.date_strings)]
			return [maker.startDate(self.date_strings[0]),
					maker.endDate(self.date_strings[1])]
	
	def make_id(self):
		if self.instant:
			return 'i_{0}'.format(self.date_strings)
		return 'd_{0}-{1}'.format(*self.date_strings)
	
	@property
	def id(self):
		if hasattr(self, '_id'):
			return self._id
		self._id = self.make_id()
		return self._id

def make_context(start, end=None):
	if end is None:
		#Instant context.
		return Context(True, start.isoformat())
	return Context(False, [start.isoformat(), end.isoformat()])