import cPickle as pick

#store it as [dict, corpus]

def unpickle(filename):
	try:
		unpicklefile = open(filename, "rb")
		unpicklelist = pick.load(unpicklefile)
		unpicklefile.close()
		return unpicklelist
	except IOError:
		return False

def pickle(filename, array):
	picklefile = open(filename,"wb+")
	pick.dump(array,picklefile)
	picklefile.close()
