from lxml.builder import ElementMaker
from lxml_helpers.helpers import xml_namespace
from common import gen_nsmap, convert_role_url, make_loc
from helpers import uid
import datetime

def make_label(fact, maker, utitle, namespace=None):
	with xml_namespace(maker, namespace, auto_convert=True) as maker:
		return maker.label(fact.label_text, **{
			'xlink:type': 'resource',
			'xlink:label': utitle,
			'xlink:role': 'http://www.xbrl.org/2003/role/label',
			'xlink:title': 'label_{0}'.format(fact.title),
			'xml:lang': 'en',
			'id': utitle,
		})

def make_labelArc(fact, maker, utitle, namespace=None):
	with xml_namespace(maker, namespace, auto_convert=True) as maker:
		return maker.labelArc(**{
			'xlink:type': 'arc',
			'xlink:arcrole': 'http://www.xbrl.org/2003/arcrole/concept-label',
			'xlink:from': fact.label,
			'xlink:to': utitle,
			'xlink:title': 'label: {0} to label_{0}'.format(fact.label)
		})

def label_serializer(serializer):
	filing = serializer.filing
	date = filing.date
	company = filing.company
	nsmap = gen_nsmap(filing, 'Label')
	maker = ElementMaker(nsmap=nsmap)

	with xml_namespace(maker, 'link', auto_convert=True) as maker:
		linkbase = maker.linkbase(**{
			#find out about this
			'xsi:schemaLocation': 'http://www.xbrl.org/2003/linkbase http://www.xbrl.org/2003/xbrl-linkbase-2003-12-31.xsd'
		})
		labellink = maker.labelLink(**{
			'xlink:type': 'extended',
			'xlink:role': 'http://www.xbrl.org/2003/role/link',
		})
		
		locs = set([])
		for (fact, unit), context, data in filing.unique_data_stream:
			if fact.href not in locs:
				labellink.append(make_loc(fact, maker, namespace='link'))
				locs.add(fact.href)

		facts = set([])
		for (fact, unit), context, data in filing.unique_data_stream:
			if (fact.label, unit) in facts:
				continue
			
			facts.add((fact.label, unit))
			utitle = 'label_{0}_{1}'.format(fact.title, uid())
			labellink.append(make_label(fact, maker, utitle, namespace='link'))
			labellink.append(make_labelArc(fact, maker, utitle, namespace='link'))

		linkbase.append(labellink)

	return linkbase
