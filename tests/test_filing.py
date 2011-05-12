from base import TestCase
from filing import Filing

class FilingTest(TestCase):
	def test_default_date(self):
		import datetime

		#test default
		self.assertEqual(datetime.date.today(), Filing().date)

		#test specified
		now = datetime.datetime.now()
		self.assertEqual(Filing(with_date=now).date, now)