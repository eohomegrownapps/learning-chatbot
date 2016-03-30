import cPickle as pick
import sys

#store it as [dict, corpus]

def unpickle(filename):
	try:
		unpicklefile = open(filename, "rb")
		unpicklelist = pick.load(unpicklefile)
		unpicklefile.close()
		return unpicklelist
	except IOError:
		return False

if __name__=="__main__":
	print unpickle(sys.stdin.readline().rstrip())
