from lxml.builder import ElementMaker
from lxml_helpers.helpers import xml_namespace, convert_attribs
from common import gen_nsmap
import datetime

def schema_serializer(serializer):
	filing = serializer.filing
	date = filing.date
	company = filing.company
	nsmap = gen_nsmap(filing, 'Schema')
	maker = ElementMaker(namespace=nsmap['xsd'], nsmap=nsmap)
	targetNamespace = '{0}{1}'.format(filing.company.url, filing.date)
	schema = maker.schema({
		'targetNamespace': targetNamespace,
		'elementFormDefault': 'qualified',
	})

	#link bases
	annotation = maker.annotation()
	appinfo = maker.appinfo()
	bases = serializer.determine_files()
	bases.remove('Instance')
	bases.remove('Schema')
	roles = {
		'Presentation': "http://www.xbrl.org/2003/role/presentationLinkbaseRef",
		'Calculation': "http://www.xbrl.org/2003/role/calculationLinkbaseRef",
		'Label': "http://www.xbrl.org/2003/role/labelLinkbaseRef",
	}
	with xml_namespace(maker, 'link'):
		for base in bases:
			appinfo.append(maker.linkbaseRef(**convert_attribs({
				'xlink:type': 'simple',
				'xlink:href': serializer.document_name(base, company),
				'xlink:role': roles[base],
				'xlink:arcrole': "http://www.w3.org/1999/xlink/properties/linkbase",
			}, nsmap)))
	
	#also need to insert roleType definitions
	
	annotation.append(appinfo)
	schema.append(annotation)

	#imports for the facts (probably have to derive this from facts)
	imports = {
		"http://www.xbrl.org/2003/instance": "http://www.xbrl.org/2003/xbrl-instance-2003-12-31.xsd",
		"http://xbrl.us/us-types/2009-01-31": "http://taxonomies.xbrl.us/us-gaap/2009/elts/us-types-2009-01-31.xsd",
		"http://xbrl.us/dei/2009-01-31": "http://taxonomies.xbrl.us/us-gaap/2009/non-gaap/dei-2009-01-31.xsd",
		"http://xbrl.us/us-gaap/negated/2008-03-31": "http://www.xbrl.org/lrr/role/negated-2008-03-31.xsd",
		"http://xbrl.us/us-gaap/2009-01-31": "http://taxonomies.xbrl.us/us-gaap/2009/elts/us-gaap-2009-01-31.xsd",
	}
	for namespace, schemaLocation in imports.items():
		#Terrible hack to get around import being a keyword
		schema.append(maker.__getattr__('import')({
			'namespace': namespace,
			'schemaLocation': schemaLocation,
		}))
	
	#Need to determine and insert custom elements
	return schema
