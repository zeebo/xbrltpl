from lxml_helpers.helpers import xml_namespace

def convert_role_url(role, filing):
	if role.startswith('http'):
		return role
	
	return '{0}/role/{1}'.format(filing_url(filing), role)

def filing_url(filing):
	#Example:
	# 'isdr': 'http://issuerdirect.com/20110620',
	return '{0}{1}'.format(filing.company.url, filing.date)

def gen_nsmap(filing, document):
	nsmap = {
		'Instance':{
			'link': 'http://www.xbrl.org/2003/linkbase',
			'xbrli': 'http://www.xbrl.org/2003/instance',
			'iso4217': 'http://www.xbrl.org/2003/iso4217',
			'xlink': 'http://www.w3.org/1999/xlink',
		},
		'Schema':{
			'link': 'http://www.xbrl.org/2003/linkbase',
			'xlink': 'http://www.w3.org/1999/xlink',
			'xbrli': 'http://www.xbrl.org/2003/instance',
			'xsd': 'http://www.w3.org/2001/XMLSchema',
		},
		'Presentation':{
			'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
			'xbrli': 'http://www.xbrl.org/2003/instance',
			'xlink': 'http://www.w3.org/1999/xlink',
		},
		'Calculation':{
			'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
			'xbrli': 'http://www.xbrl.org/2003/instance',
			'xlink': 'http://www.w3.org/1999/xlink',
		},
		'Label':{
			'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
			'link': 'http://www.xbrl.org/2003/linkbase',
			'xbrli': 'http://www.xbrl.org/2003/instance',
			'xlink': 'http://www.w3.org/1999/xlink',
			'xml': 'http://www.w3.org/XML/1998/namespace',
		},
	}[document]
	nsmap[filing.company.ticker] = filing_url(filing)
	return nsmap

def make_loc(fact, maker, namespace=None):
	with xml_namespace(maker, namespace, auto_convert=True) as maker:
		return maker.loc(**{
			'xlink:type': 'locator',
			'xlink:href': fact.href,
			'xlink:label': fact.label,
			'xlink:title': fact.title,
		})

