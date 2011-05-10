from base import TestCase
from datas.matrix import Matrix

import random

class MatrixTest(TestCase):
	def setUp(self):
		self.m = Matrix()

	def test_two_dimensional(self):
		self.assertRaises(IndexError, self.m.__getitem__, (1,2,3))
	
	def test_default(self):
		self.assertEqual(self.m[0,0], None)
		self.m.default = 0
		self.assertEqual(self.m[0,0], 0)

	def test_sets(self):
		#perform 30 random index lookups
		indicies = set([])
		while len(indicies) < 30:
			indicies.add(( random.randint(0,50), random.randint(0, 50) ))
		for e, (a,b) in enumerate(indicies):
			self.assertEqual(self.m[a,b], None)
			self.m[a,b] = e
			self.assertEqual(self.m[a,b], e)
	
	def test_negative_fails(self):
		for function in ['get', 'del']:
			attr = getattr(self.m, '__%sitem__' % function)
			self.assertRaises(IndexError, attr, (-1, 2))
			self.assertRaises(IndexError, attr, (2, -1))
			self.assertRaises(IndexError, attr, (-2, 5))
		
		self.assertRaises(IndexError, self.m.__setitem__, (-1, 2), 0)
		self.assertRaises(IndexError, self.m.__setitem__, (2, -1), 0)
		self.assertRaises(IndexError, self.m.__setitem__, (-2, 5), 0)
	
	def test_delete_index(self):
		self.m[1,5] = 6
		self.assertEqual(self.m[1,5], 6)
		del self.m[1,5]
		self.assertEqual(self.m[1,5], None)
	
