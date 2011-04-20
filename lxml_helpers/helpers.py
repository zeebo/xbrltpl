import contextlib

@contextlib.contextmanager
def xml_namespace(maker, ns):
	old = maker._namespace
	maker._namespace = '{{{0}}}'.format(maker._nsmap[ns])
	yield
	maker._namespace = old

def make_attrib(attrib, nsmap):
	parts = attrib.split(':')
	return '{{{0}}}{1}'.format(nsmap[parts[0]], parts[1])

def convert_attribs(attribs, nsmap):
	new_attribs = {}
	for key in attribs:
		new_attribs[make_attrib(key, nsmap)] = attribs[key]
	return new_attribs
