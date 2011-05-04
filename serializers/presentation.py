from lxml.builder import ElementMaker
from lxml_helpers.helpers import xml_namespace
from common import gen_nsmap, convert_role_url
import datetime

def presentation_serializer(serializer):
	pass

def chart_serializer(chart, filing, maker):
	nsmap = maker._nsmap
	with xml_namespace(maker, None, auto_convert=True) as maker:
		role = convert_role_url(chart.role, filing)
		link = maker.presentationLink(**{
			'xlink:type': 'extended',
			'xlink:role': role,
		})

		parent = maker.loc(**{
			
		})