import cPickle as pickle

#store it as [dict, corpus]

def unpickle(filename):
	unpicklefile = open(filename, "rb")
	unpicklelist = pickle.load(unpicklefile)
	unpicklefile.close()
	return unpicklelist

def pickle(filename, array):
	picklefile = open(filename,"wb+")
	pickle.dump(array,picklefile)
	picklefile.close()
