import random

def uid(length=10, gens={}):
	bits = random.getrandbits(4*length)
	while bits in gens:
		bits = random.getrandbits(4*length)
	gens[bits] = True
	return "{0:0{1}X}".format(bits, length)
