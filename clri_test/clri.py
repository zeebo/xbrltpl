#hack to get the package
import sys
sys.path.append('/home/zeebo/Code/envs/xbrltpl/xbrltpl')

from container.template import Template
from container.filing import Filing
from container.chart import Chart
from datas.context import make_context
from datas.unit import Unit
from datas.fact import Fact
from serializers.serializer import Serializer, lxml_to_text
import datetime

class Company(object):
	cik = '1362516'
	url = 'http://cleartronic.com/'
	ticker = 'clri'

mar_31_2011 = make_context(datetime.date(2011, 3, 31))
sept_30_2010 = make_context(datetime.date(2010, 9, 30))
jan_to_mar_2011 = make_context(datetime.date(2011, 1, 1), datetime.date(2011, 3, 31))
sept_to_mar_2011 = make_context(datetime.date(2010, 9, 30), datetime.date(2011, 3, 31))
jan_to_mar_2010 = make_context(datetime.date(2010, 1, 1), datetime.date(2010, 3, 31))
sept_to_mar_2010 = make_context(datetime.date(2009, 9, 30), datetime.date(2010, 3, 31))

dollars = Unit('USD', 'iso4217:USD')

def convert(thing):
	if thing == '-':
		return ''
	if thing[0] == '(' or thing[0] == '-':
		return -1 * int(filter(lambda x: x.isdigit(), thing))
	return int(filter(lambda x: x.isdigit(), thing))

def cleaned(thing):
	return filter(lambda x: x.isalpha() or x == ' ', thing)

def make_label(thing):
	return ''.join(it.capitalize() for it in cleaned(thing).split(' '))

def make_chart(data, contexts):
	temp = Template()
	for context in contexts:
		temp.add_context(context)

	for line in data:
		if '\t' not in line:
			temp.add_fact(Fact(label=make_label(line), namespace='us-gaap', abstract=True), dollars)
		else:
			title = line.split('\t')[0]
			fact = Fact(label=make_label(title), namespace='us-gaap')
			temp.add_fact(fact, dollars)
	
	chart = Chart(with_template=temp)

	for i, line in enumerate(data):
		if '\t' in line:
			values = line.split('\t')[1:]
			for context, item in zip(contexts, values):
				chart[i, context] = convert(item)
	
	return chart

balance_sheet_chart = make_chart('''Current assets
Cash	268,790	22,348
Accounts receivable, net	25,610	5,019
Inventory	63,990	51,076
Prepaid expenses and other current assets	14,756	32,407
Total current assets	373,146	110,850
Property and equipment, net 	17,905	25,270
Total assets	391,051	136,120
Current liabilities
Accounts payable	228,693	243,887
Accrued expenses	144,934	79,950
Deferred revenue, current portion	22,219	8,503
Notes payable - stockholders	119,806	121,180
Total current liabilities	515,652	453,520
Long Term Liabilities
Notes payable - stockholders	25,000	25,000
Deferred revenue, net of current portion	10,003	1,063
Total long term liabilities	35,003	26,063
Total liabilities	550,655	479,583
Stockholders' equity (deficit)
Preferred stock	900	250
Common stocky	132,308	132,308
Additional paid-in capital	6,656,902	6,007,553
Accumulated Deficit	(6,949,714	(6,483,574)
Total stockholders' equity (deficit)	(159,604	(343,463)
Total liabilities and stockholders' equity (deficit)	391,051	136,120'''.split('\n'), contexts=[mar_31_2011, sept_30_2010])

stmt_of_ops = make_chart('''Revenue	$128,358	$23,127	$308,800	$90,291
Cost of Revenue	68,442	11,040	154,537	43,387
Gross Profit	59,916	12,087	154,263	46,904
Operating Expenses
Selling expenses	41,401	34,440	75,878	49,677
Administrative expenses	237,599	215,325	446,112	374,284
Research and development	29,072	21,985	55,470	66,861
Depreciation	3,393	6,689	7,364	14,540
Total Operating Expenses	311,465	278,439	584,824	505,362
Other (Expenses)	(19,493)	(19,167)	(35,580)	(30,327)
Net loss	(271,042)	(285,519)	(466,141)	(488,785)
(Loss) per Common Share	$(0.002)	$(0.003)	$(0.004)	$(0.005)
(Loss) per Common Share basic and diluted	$(0.002)	$(0.003)	$(0.004)	$(0.005)
Weighted Average of Shares Outstanding basic and diluted	132,307,758	101,677,485	132,307,758	89,596,677'''.split('\n'), contexts=[jan_to_mar_2011, jan_to_mar_2010, sept_to_mar_2011, sept_to_mar_2010])

cash_flow = make_chart('''NET LOSS	$(466,141)	$(488,785)
Depreciation	7,365	14,540
Common stock and warrants issued for services	-	118,750
Loss on settlement and disposal of assets	-	4,220
Amortization of notes payable discount	937	17,942
Accounts receivable	(20,591)	(165)
Inventory	(12,914)	(27,339)
Prepaid expenses and other current assets	16,714	(8,333)
Accounts payable	(15,194)	(40,095)
Accrued expenses	64,984	95,269
Deferred revenue	22,656	(9,626)
Net Cash Used in Operating Activities	(402,184)	(323,622)
Purchase of property and equipment	-	(4,004)
Net Cash Provided by Investing Activities:	-	(4,004)
Cash Flows From Financing Activities
Principal payments on notes payable	(1,374)	-
Proceeds from notes payable, net	-	39,900
Proceeds from issuance of common stock and warrants	-	300,000
Proceeds from issuance of preferred stock	650,000	-
Net Cash Provided by Financing Activities	648,626	339,900
Net Increase In Cash	246,442	12,274
Cash - Beginning of Period	22,348	8,273
Cash - End of Period	$268,790	$20,547
Cash paid for interest	$11,781	$6,313'''.split('\n'), contexts=[sept_to_mar_2011, sept_to_mar_2010])

clri = Filing(with_charts=[balance_sheet_chart, stmt_of_ops, cash_flow], with_company=Company)

serializer = Serializer(clri)

import os
os.chdir(os.path.dirname(__file__))

for document in ['Instance', 'Presentation', 'Label', 'Schema']:
	text = serializer.serialize(document, formatter=lxml_to_text)
	handle = open(serializer.document_name(document), 'w')
	handle.write(text)
	handle.close()