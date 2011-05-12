from lxml.builder import ElementMaker
from lxml_helpers.helpers import xml_namespace
from common import gen_nsmap, convert_role_url
import datetime

def presentation_serializer(serializer):
	filing = serializer.filing
	date = filing.date
	company = filing.company
	nsmap = gen_nsmap(filing, 'Presentation')
	maker = ElementMaker(nsmap=nsmap)

	with xml_namespace(maker, None, auto_convert=True) as maker:
		linkbase = maker.linkbase(**{
			#find out about this
			'xsi:schemaLocation': 'http://www.xbrl.org/2003/linkbase http://www.xbrl.org/2003/xbrl-linkbase-2003-12-31.xsd'
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
		link = maker.presentationLink(**{
			'xlink:type': 'extended',
			'xlink:role': role,
		})

		link.append(chart.make_loc(maker))

		class ParentObject(object):
			label = 'stub'

		for order, (n_parent, n_child) in enumerate(chart.walk_tree()):
			if n_parent is None:
				n_parent = (ParentObject, None)
			
			n_child, n_parent = n_child[0], n_parent[0]

			link.append(n_child.make_loc(maker))
			link.append(n_child.make_presentation(n_parent, order, maker))
	
	return link



# Facts should be able to create their own locs
# presentationArcs are derived from data in the chart
#<loc 
#	xlink:type="locator"
#	xlink:href="http://taxonomies.xbrl.us/us-gaap/2009/non-gaap/dei-2009-01-31.xsd#dei_DocumentPeriodEndDate"
#	xlink:label="DocumentPeriodEndDate"
#	xlink:title="DocumentPeriodEndDate"
#/>


# Presentationarcs go from label to label