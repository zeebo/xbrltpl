from template import Template
from filing import Filing
from chart import Chart
from datas.context import make_context
from datas.unit import Unit
from datas.fact import Fact
from serializers.serializer import Serializer, lxml_to_text
import datetime

class Company(object):
	cik = '73245098723'
	url = 'http://issuerdirect.com/'
	ticker = 'isdr'

c1 = make_context(datetime.date(2008, 5, 12))
c2 = make_context(datetime.date(2008, 5, 12), datetime.date(2008, 11, 12))
c3 = make_context(datetime.date(2020, 6, 30), datetime.date(2021, 12, 1))

u1 = Unit('id1', 'measure1')
u2 = Unit('id2', 'measure2')
f1, f2 = Fact(), Fact()

t = Template()
t.add_context(c1)
t.add_context(c2)
t.add_context(c3)
t.add_fact(f1, u1)
t.add_fact(f2, u2)

c = Chart(with_template=t)
c[(f1, u1), c1] = 100
c[(f1, u1), c2] = 200
c[(f1, u1), c3] = 300
c[(f2, u2), c1] = 400
c[(f2, u2), c2] = 500
c[(f2, u2), c3] = 600

f = Filing(with_charts=[c], with_company=Company)

s = Serializer(f)
print s.serialize('Instance', formatter=lxml_to_text)