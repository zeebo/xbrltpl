from lxml.builder import ElementMaker
from lxml_helpers.helpers import xml_namespace, convert_attribs
from common import gen_nsmap, convert_role_url
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
	with xml_namespace(maker, 'link', auto_convert=True) as maker:
		for base in bases:
			appinfo.append(maker.linkbaseRef(**{
				'xlink:type': 'simple',
				'xlink:href': serializer.document_name(base),
				'xlink:role': roles[base],
				'xlink:arcrole': "http://www.w3.org/1999/xlink/properties/linkbase",
			}))

		for i, chart in enumerate(filing.charts):
			roleType = maker.roleType(**{
				'roleURI': convert_role_url(chart.role, filing),
				'id': chart.role
			})

			roleType.append(maker.definition('%04d - %s' % (10*(i+1), chart.role) ))
			roleType.append(maker.usedOn('link:presentationLink'))

			appinfo.append(roleType)
	
	annotation.append(appinfo)
	schema.append(annotation)

	#imports for the facts (probably have to derive this from facts)
	imports = {
		"http://www.xbrl.org/2003/instance": "http://www.xbrl.org/2003/xbrl-instance-2003-12-31.xsd",
		"http://xbrl.us/us-types/2009-01-31": "http://taxonomies.xbrl.us/us-gaap/2009/elts/us-types-2009-01-31.xsd",
	}
	for namespace, schemaLocation in imports.items():
		#Terrible hack to get around import being a keyword
		schema.append(maker.__getattr__('import')({
			'namespace': namespace,
			'schemaLocation': schemaLocation,
		}))
	
	#Create a custom element for everything
	fact_table = {}
	for (fact, _), _, _ in filing.data_stream:
		fact_table[fact.label] = fact
	
	facts = fact_table.values()


	with xml_namespace(maker, 'xsd', auto_convert=True) as maker:
		#append facts for the chart abstract facts
		for chart in filing.charts:
			fact = chart.loc_fact
			schema.append(maker.element(**{
				'id': fact.label,
				'name': fact.label,
				'type': 'xbrli:stringItemType',
				'substitutionGroup': 'xbrli:item',
				'nillable': 'true',
				'abstract': 'true',
				'xbrli:periodType': 'duration',
			}))
		
		#append the rest of the facts we need to define
		for fact in facts:
			schema.append(maker.element(**{
				'id': fact.label,
				'name': fact.label,
				'nillable': 'true',
				'substitutionGroup': 'xbrli:item',
				'type': 'xbrli:monetaryItemType',
				'xbrli:periodType': fact.period,
			}))
	
	return schema
