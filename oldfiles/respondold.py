from __future__ import division
import sys
#please only give me sentences as list

alphabet = "abcdefghijklmnopqrstuvwxyz"

class Responder:
	def __init__(self,corpus,dictionary):
		self.corpus = corpus
		self.dictionary = dictionary

	def response(self, sentence):
		sentencesort = []
		for i in range(0,len(sentence)):
			commonval = 0
			dictentry = self.searchdict(sentence[i])
			#print dictentry
			if dictentry != False:
				sentencesort.append([sentence[i],dictentry])
		#print sentencesort
		sentencesort = sorted(sentencesort, key=lambda x: x[1])
		#print sentencesort
		#TODO: NN implementation. Weights: most words common vs commonness of words
		sentencesortnew = []
		for i in sentencesort:
			sentencesortnew.append(i[0])
		#print sentencesortnew
		if len(sentencesortnew) == 0:
			return False
		#print "commonness -------------------------"
		return self.common(sentencesortnew,self.corpus)

	#Test algorithm
	def responserate(self, sentence):
		maximum = None
		#corpus = [[["hello"],["hi"],0],[["hi"],["hello"],1]]
		#[[corpusentries],rating]
		for i in self.corpus:
			rating = self.rate(sentence,i[0])
			if maximum != None:
				if maximum[1]<rating:
					maximum = [[i],rating]
				elif maximum[1]==rating:
					maximum[0].append(i)
			else:
				maximum = [[i],rating]
		#print maximum
		return maximum[0]

	def common(self, s, corpu):
		#print s
		#returns corpus consisting of [["statement"],["response"]]
		if len(corpu) == 1:
			return corpu
		if len(s) == 0:
			if len(corpu) > 0:
				return corpu
			else:
				return None
		tempcorp = self.searchcorpus(s[0],corpu)
		if tempcorp != False:
			corpu = tempcorp
			#print corpu
		s.pop(0)
		return self.common(s, corpu)

	def listify(self, sentence):
		sentence = list(sentence.lower())
		#print sentence
		result = []
		alphalist = list(alphabet)
		word = ""
		flag = False
		for i in sentence:
			if flag == False:	
				if i == " ":
					result.append(word)
					word = ""
				if i in alphalist:
					word = word+i
				if i == "\\":
					flag = True 
			else:
				flag = False
		if word != "":
			result.append(word)
		#print result
		return result

	def searchdict(self, word):
		for i in self.dictionary:
			if word == i[0]:
				return i[1]
		return False

	#def searchsentences(word, sentences):
	#	for i in sentences:
	#		if word in 

	def searchcorpus(self, word, corp):
		result = []
		for i in corp:
			stripped = i[0]
			if word in stripped:
				result.append(i)
		if len(result) == 0:
			return False
		return result

	def sentenceincorpus(self, sent):
		result = []
		for i in self.corpus:
			stripped = i[0]
			if sent == stripped:
				return True
		return False

	def dictlen(self):
		totalfreq = 0
		for i in self.dictionary:
			totalfreq += i[1]
		return totalfreq

	"""def rate(self, sentencea, sentenceb):
		#sentences as list, please
		commonwords = []
		for i in sentencea:
			if i in sentenceb and i not in commonwords:
				commonwords.append(i)
		#print commonwords
		rate = 0
		for word in commonwords:
			freq = self.searchdict(word)/self.dictlen()
			#print freq
			rate = rate+freq
		length = len(commonwords)
		#print rate
		sentencediff = abs(len(sentencea)-len(sentenceb))
		sentencemean = sentencediff/((len(sentencea)+len(sentenceb))/2)
		rate = (length-rate)/((len(sentencea)+len(sentenceb))/2)
		rate = rate + sentencemean
		return rate"""

	def rate(self, sentencea, sentenceb):
		#print "rate"
		#sentences as list, please
		commonwords = []
		for i in sentencea:
			if i in sentenceb and i not in commonwords:
				commonwords.append(i)
		#print commonwords
		rate = 0
		for word in commonwords:
			freq = self.searchdict(word)/self.dictlen()
			#print freq
			rate = rate+freq
		length = len(commonwords)
		#print rate
		sentencediff = abs(len(sentencea)-len(sentenceb))
		#print sentencediff
		sentencemean = sentencediff/((len(sentencea)+len(sentenceb))/2)
		#print sentencemean
		rate = (length-rate)/((len(sentencea)+len(sentenceb))/2)
		#print rate
		rate = rate - (sentencemean/5)
		return rate

	def howcommon(self, sentence):
		result = 0
		for i in sentence:
			length = self.searchdict(i)
			if length != False:
				result += length
		return result
		
	def updatecorpus(corpus):
		self.corpus = corpus

	def updatedict(dictionary):
		self.dictionary = dictionary


if __name__ == '__main__':
	sentencea = sys.stdin.readline()
	sentenceb = sys.stdin.readline()
	corpus = []
	dictionary = [['do', 1], ['you', 11], ['like', 2], ['fish', 2], ['yes', 1], ['i', 12], ['hate', 1], ['potatoes', 1], ['no', 1], ['dont', 3], ['have', 4], ['to', 4], ['go', 2], ['the', 4], ['bathroom', 2], ['drink', 2], ['too', 4], ['much', 4], ['coffee', 4], ['but', 2], ['love', 2], ['well', 2], ['its', 2], ['your', 2], ['life', 2], ['eat', 2], ['chocolate', 2], ['think', 4], ['so', 2], ['looked', 2], ['in', 2], ['mirror', 2], ['do', 1], ['im', 2], ['getting', 2], ['fat', 2], ['do', 1], ['didnt', 2], ['say', 4], ['that', 2], ['what', 2], ['did', 2], ['said', 1]]
	Respond = Responder(corpus, dictionary)

	print Respond.rate(Respond.listify(sentencea), Respond.listify(sentenceb))

