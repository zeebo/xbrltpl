from container.template import Template
from container.filing import Filing
from container.chart import Chart
from datas.context import make_context
from datas.unit import Unit
from datas.fact import Fact
from serializers.serializer import Serializer, lxml_to_text
import datetime

class Company(object):
	cik = '0000843006'
	url = 'http://issuerdirect.com/'
	ticker = 'isdr'

c1 = make_context(datetime.date(2009, 12, 31))

u1 = Unit('USD', 'iso4217:USD')
u2 = Unit('Shares', 'xbrli:shares')

f1 = Fact(label='AssetsCurrent', namespace='isdr')
f2 = Fact(label='OtherAssetsCurrent', namespace='isdr')
f3 = Fact(with_calc=[(f1, 1), (f2, 1)], label='Assets', namespace='isdr')
  
t = Template()
t.add_context(c1)
t.add_fact(f1, u1, parent=(f3, u1))
t.add_fact(f2, u1, parent=(f3, u1))
t.add_fact(f3, u1)

c = Chart(with_template=t, title='DocumentSomethingOrOther')
c[(f1, u1), c1] = 323555
c[(f2, u1), c1] = 19201
c[(f3, u1), c1] = 465005

f = Filing(with_charts=[c], with_company=Company)

s = Serializer(f)
print s.serialize('Presentation', formatter=lxml_to_text)