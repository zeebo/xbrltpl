import contextlib

@contextlib.contextmanager
def xml_namespace(maker, ns, auto_convert=False):
	old = maker._namespace
	if ns is None:
		maker._namespace = ''
	else:
		maker._namespace = '{{{0}}}'.format(maker._nsmap[ns])
	
	if auto_convert:
		yield Wrapper(maker)
	else:
		yield maker
	maker._namespace = old

def kwarg_wrapper(func, maker):
	def dec(*args, **kwargs):
		return func(*args, **convert_attribs(kwargs, maker._nsmap))
	return dec

class Wrapper(object):
	def __init__(self, maker):
		self._maker = maker
	def __getattr__(self, name):
		if name == '_nsmap':
			return self._maker._nsmap
		if name == '_namespace':
			return self._maker._namespace
		
		if isinstance(self._maker, Wrapper):
			return self._maker.__getattr__(name)
		return kwarg_wrapper(self._maker.__getattr__(name), self._maker)

@contextlib.contextmanager
def auto_convert(maker):
	yield Wrapper(maker)

def make_attrib(attrib, nsmap):
	if ':' in attrib:
		parts = attrib.split(':')
		return '{{{0}}}{1}'.format(nsmap[parts[0]], parts[1])
	return attrib

def convert_attribs(attribs, nsmap):
	new_attribs = {}
	for key in attribs:
		new_attribs[make_attrib(key, nsmap)] = attribs[key]
	return new_attribs
