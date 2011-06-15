from container.filing import Filing
from calculation import calculation_serializer
from definition import definition_serializer
from instance import instance_serializer
from label import label_serializer
from presentation import presentation_serializer
from schema import schema_serializer

from datetime import date

import lxml
from lxml import etree

#Serializer determines which files need to be serialized and dispatches
#to the appropriate objects that serialize that type of file with a
#specific Filing object

#Documents:
#	Instance
#	Schema
#	Calculation Linkbase
#	Definition Linkbase
#	Label Linkbase
#	Presentation Linkbase

NAME_MAP = {
	'Instance': instance_serializer,
	'Schema': schema_serializer,
	'Calculation': calculation_serializer,
	'Definition': definition_serializer,
	'Label': label_serializer,
	'Presentation': presentation_serializer,
}

def lxml_to_text(nodes):
	"""Takes the lxml nodes and turns it into text"""
	return etree.tostring(nodes, pretty_print=True)

def nodes(x):
	"""Do-nothing function. lambda x: x"""
	return x

class Serializer(object):
	def __init__(self, filing):
		assert isinstance(filing, Filing)
		self.filing = filing
	
	def format_date(self, given_date=None):
		if given_date is None:
			given_date = self.filing.date
		
		return given_date.strftime('%Y%m%d')
	
	@property
	def date(self):
		return self.format_date()
	
	def document_name(self, document):
		#Determined by SEC on http://sec.gov/info/edgar/edgarfm-vol2-v16.pdf
		#page 221 (6-5), section 6.6.3
		template_map = {
			'Instance': '{0}-{1}.xml',
			'Schema': '{0}-{1}.xsd',
			'Calculation': '{0}-{1}_cal.xml',
			'Definition': '{0}-{1}_def.xml',
			'Label': '{0}-{1}_lab.xml',
			'Presentation': '{0}-{1}_pre.xml',
		}

		template = template_map[document]
		return template.format(self.filing.company.ticker, self.date)

	def determine_files(self):
		"""Determines the documents that must be created
		for a valid sec filing."""
		others = []

		for (fact, unit), context, value in self.filing.data_stream:
			if fact.is_calc:
				others.append('Calculation')
				break

		return ['Instance', 'Schema', 'Presentation', 'Label'] + others
	
	def serialize(self, document, formatter=nodes):
		"""Returns the serialized xml data in the specified format.

		arguments:
			name		type	description
			----        ----    -----------
			document:	string	Name of document to be serialized (returned by determine_files)
			formatter:	(func)	Formatter. Should take lxml nodes as input, and return whatever. If you want lxml nodes, use (lambda x: x)
		"""

		document_serializer = NAME_MAP[document]
		data = document_serializer(serializer=self)

		return formatter(data)
	
	def serialized_docs(self, formatter=nodes):
		for document in self.determine_files():
			yield self.document_name(document), self.serialize(document, formatter=formatter)
	
	def namespaces_for(document):
		#queries self.filing to figure out what namespaces will be defined
		#in the document. for now return the company namespace
		nsmap = {}

		nsmap[self.filing.company.ticker] = '{0}{1}'.format(self.filing.company.url, self.date)
		return nsmap
