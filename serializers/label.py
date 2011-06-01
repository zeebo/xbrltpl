from lxml.builder import ElementMaker
from lxml_helpers.helpers import xml_namespace
from common import gen_nsmap, convert_role_url, make_loc
import datetime

def make_label(fact, maker, namespace=None):
	with xml_namespace(maker, namespace, auto_convert=True) as maker:
		return maker.label(fact.label_text, **{
			'xlink:type': 'resource',
			'xlink:label': 'label_{0}'.format(fact.label),
			'xlink:role': 'http://www.xbrl.org/2003/role/label',
			'xlink:title': 'label_{0}'.format(fact.title),
			'xml:lang': 'en',
			'id': 'label_{0}'.format(fact.label),
		})

def make_labelArc(fact, maker, namespace=None):
	with xml_namespace(maker, namespace, auto_convert=True) as maker:
		return maker.labelArc(**{
			'xlink:type': 'arc',
			'xlink:arcrole': 'http://www.xbrl.org/2003/arcrole/concept-label',
			'xlink:from': fact.label,
			'xlink:to': 'label_{0}'.format(fact.label),
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
		
		for (fact, unit), context, data in filing.data_stream:
			labellink.append(make_loc(fact, maker, namespace='link'))
			labellink.append(make_label(fact, maker, namespace='link'))
			labellink.append(make_labelArc(fact, maker, namespace='link'))

		linkbase.append(labellink)

	return linkbase
