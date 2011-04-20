from lxml.builder import ElementMaker
from lxml_helpers.helpers import xml_namespace, convert_attribs
import datetime

def instance_serializer(filing, company, serializer):
	#looks like
	#<xbrli:xbrl [namespaces]>
	#<link:schemaRef to xsd document>
	#[<contexts>]
	#[<units>]
	#[<facts>]
	#</xbrli:xbrl>
	date = serializer.format_date(datetime.date.today())

	nsmap = {
		'link': 'http://www.xbrl.org/2003/linkbase',
		'us-gaap': 'http://xbrl.us/us-gaap/2009-01-31',
		'ref': 'http://www.xbrl.org/2006/ref',
		'us-types': 'http://xbrl.us/us-types/2009-01-31',
		'xbrldt': 'http://xbrl.org/2005/xbrldt',
		'dei': 'http://xbrl.us/dei/2009-01-31',
		'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
		'xbrli': 'http://www.xbrl.org/2003/instance',
		'negated': 'http://xbrl.us/us-gaap/negated/2008-03-31',
		'iso4217': 'http://www.xbrl.org/2003/iso4217',
		'us-roles': 'http://xbrl.us/us-roles/2009-01-31',
		'xlink': 'http://www.w3.org/1999/xlink',

		#Example:
		# 'isdr': 'http://issuerdirect.com/20110620',
		company.ticker: '{0}{1}'.format(company.url, date),
	}
	
	maker = ElementMaker(namespace=nsmap['xbrli'], nsmap=nsmap)

	xbrl = maker.xbrl()
	with xml_namespace(maker, 'link'):
		schemaRef = maker.schemaRef(**convert_attribs({
			'xlink:type': 'simple',
			'xlink:href': serializer.document_name('Schema', company),
		}, nsmap))
	
	xbrl.append(schemaRef)

	#Loop over contexts, appending to xbrl
	for context in filing.contexts:
		xbrl.append(context.serialize(maker, company.cik))
	
	#Loop over units, appending to xbrl
	for unit in filing.units:
		xbrl.append(unit.serialize(maker))
	
	#Loop over facts appending to xbrl
	#for fact, _ in filing.facts:
	#	xblr.append(fact.serialize(maker))

	return xbrl
