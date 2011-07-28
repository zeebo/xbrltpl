from lxml.builder import ElementMaker
from lxml_helpers.helpers import xml_namespace
from common import gen_nsmap, convert_role_url, make_loc
import datetime

def make_calculationArc(child, parent, order, weight, maker, namespace=None):
	with xml_namespace(maker, namespace, auto_convert=True) as maker:
		return maker.presentationArc(**{
			'xlink:type': 'arc',
			'xlink:arcrole': 'http://www.xbrl.org/2003/arcrole/summation-item',
			'xlink:from': parent.label,
			'xlink:to': child.label,
			'xlink:title': 'calculation: {0} to {1}'.format(
					parent.label, child.label
				),
			'order': '{0:.1f}'.format(order),
			'weight': '{0:.1f}'.format(weight),
		})


def calculation_serializer(serializer):
	filing = serializer.filing
	date = filing.date
	company = filing.company
	nsmap = gen_nsmap(filing, 'Calculation')
	maker = ElementMaker(nsmap=nsmap)

	with xml_namespace(maker, None, auto_convert=True) as maker:
		linkbase = maker.linkbase(**{
			#find out about this
			'xsi:schemaLocation': 'http://www.xbrl.org/2003/linkbase http://www.xbrl.org/2003/xbrl-linkbase-2003-12-31.xsd',
			'xmlns': 'http://www.xbrl.org/2003/linkbase',
		})
		for chart in filing.charts:
			roleRef = maker.roleRef(**{
				'roleURI': convert_role_url(chart.role, filing),
				'xlink:type': 'simple',
				'xlink:href': '{0}#{1}'.format(
						serializer.document_name('Schema'),
						chart.role
					)
			})

			linkbase.append(roleRef)
			linkbase.append(chart_serializer(chart, filing, maker))
	
	return linkbase

def chart_serializer(chart, filing, maker):
	with xml_namespace(maker, None, auto_convert=True) as maker:
		role = convert_role_url(chart.role, filing)
		link = maker.calculationLink(**{
			'xlink:type': 'extended',
			'xlink:role': role,
		})

		for calc_fact in chart.calculation_facts:
			link.append(make_loc(calc_fact, maker))

			for order, (fact, weight) in enumerate(calc_fact.calc_items):
				link.append(make_loc(fact, maker))
				link.append(make_calculationArc(fact, calc_fact, order+1, weight, maker))
	
	return link
