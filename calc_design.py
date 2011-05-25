import random
import operator
from functools import wraps

def uid(length=10):
	return "{0:0{1}X}".format(random.getrandbits(4*length), length)

def class_gen(op, repr):
	class NewClass(object):
		def __repr__(self): return repr
		def __call__(self, a, b): return op(a, b)
	return NewClass()

add = class_gen(operator.add, '+')
mul = class_gen(operator.mul, '*')

def guarded(function):
	@wraps(function)
	def new_func(self, other):
		if not isinstance(other, type(self)):
			return NotImplemented
		return function(self, other)
	return new_func

class Calc(object):
	def __init__(self, name=None, op=None, first=None, second=None):
		if name is None:
			name = '({0}{1}{2})'.format(first.name,op,second.name)
		
		self.name = name
		self.op = op
		self.first = first
		self.second = second
		self.id = uid()

	def __repr__(self):
		return '{0}:{1}'.format(self.name, self.id)
	
	@guarded
	def __add__(self, other):
		return Calc(op=add, first=self, second=other)
	
	@guarded
	def __mul__(self, other):
		return Calc(op=mul, first=self, second=other)
	
	def tree_gen(self, seen=None):
		if seen is None:
			seen = {None: True}
		if self.id in seen:
			return
		seen[self.id] = True

		if self.first not in seen:
			for x in self.first.tree_gen(seen):
				yield x
		
		if self.second not in seen:
			for x in self.second.tree_gen(seen):
				yield x

		yield self, self.first, self.op, self.second

	@property
	def tree(self):
		return list(self.tree_gen())
	
a,b,c,d,e = (Calc(name=x) for x in 'abcde')

def fancy_op(a, b,):
	op = random.choice([mul, add])
	return op(a, b)

for thing in (b+b*b*b*b).tree:
	print thing
print '-'
for thing in reduce(fancy_op, [e]*10).tree:
	print thing

#things: add negation