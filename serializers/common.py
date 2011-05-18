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
		},
		'Schema':{
			'xsd': 'http://www.w3.org/2001/XMLSchema',
			'us-gaap-std': 'http://xbrl.us/us-gaap-std/2009-01-31',
			'stm-all-ci': 'http://xbrl.us/ci/stm-all/2009-01-31',
			'ref': 'http://www.xbrl.org/2006/ref',
			'us-roles': 'http://xbrl.us/us-roles/2009-01-31',
			'xbrldt': 'http://xbrl.org/2005/xbrldt',
			'xl': 'http://www.xbrl.org/2003/XLink',
			'ci-scf-indir': 'http://xbrl.us/stm/ci/scf-indir/2009-01-31',
			'ci-soc': 'http://xbrl.us/stm/ci/soc/2009-01-31',
			'ci-sheci': 'http://xbrl.us/stm/ci/sheci/2009-01-31',
			'ci-com': 'http://xbrl.us/stm/ci/com/2009-01-31',
			'dei': 'http://xbrl.us/dei/2009-01-31',
			'ci-spc': 'http://xbrl.us/stm/ci/spc/2009-01-31',
			'us-gaap-att': 'http://xbrl.us/us-gaap/attributes',
			'us-gaap-all': 'http://xbrl.us/us-gaap-all/2009-01-31',
			'link': 'http://www.xbrl.org/2003/linkbase',
			'stm-ci': 'http://xbrl.us/ci/stm/2009-01-31',
			'xlink': 'http://www.w3.org/1999/xlink',
			'ci-scf-dir': 'http://xbrl.us/stm/ci/scf-dir/2009-01-31',
			'ci-soi': 'http://xbrl.us/stm/ci/soi/2009-01-31',
			'dei-std': 'http://xbrl.us/dei-std/2009-01-31',
			'us-gaap': 'http://xbrl.us/us-gaap/2009-01-31',
			'ci-sfp-cls': 'http://xbrl.us/stm/ci/sfp-cls/2009-01-31',
			'us-types': 'http://xbrl.us/us-types/2009-01-31',
			'xbrli': 'http://www.xbrl.org/2003/instance',
		},
		'Presentation':{
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
		}
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

def make_label(fact, maker, namespace=None):
	with xml_namespace(maker, namespace, auto_convert=True) as maker:
		return maker.label(fact.label_text, **{
			'xlink:type': 'resource',
			'xlink:label': 'label_{0}'.format(fact.label),
			'xlink:role': 'http://www.xbrl.org/2003/role/label',
			'xlink:title': 'label_{0}'.format(fact.label),
			'xml:lang': 'en',
			'id': 'label_{0}'.format(fact.label),
		})

def make_presentationArc(child, parent, order, maker, namespace=None):
	with xml_namespace(maker, namespace, auto_convert=True) as maker:
		return maker.presentationArc(**{
			'xlink:type': 'arc',
			'xlink:arcrole': 'http://www.xbrl.org/2003/arcrole/parent-child',
			'xlink:from': parent.label,
			'xlink:to': child.label,
			'xlink:title': 'presentation: {0} to {1}'.format(
					parent.label, child.label
				),
			'use': 'optional',
			'order': '{0:.1f}'.format(order)
		})

def make_labelArc(fact, maker, namespace=None):
	with xml_namespace(maker, namespace, auto_convert=True) as maker:
		return maker.labelArc(**{
			'xlink:type': 'arc',
			'xlink:arcrole': 'http://www.xbrl.org/2003/arcrole/concept-label',
			'xlink:from': 'label_{0}'.format(fact.label),
			'xlink:to': fact.label,
			'xlink:title': 'label: {0} to label_{0}'.format(fact.label)
		})