def gen_nsmap(filing):
	return {
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
		#Example:
		# 'isdr': 'http://issuerdirect.com/20110620',
		filing.company.ticker: '{0}{1}'.format(filing.company.url, filing.date),
	}