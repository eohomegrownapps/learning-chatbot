import sys

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

	def rate(self, sentencea, sentenceb):
		#sentences as list, please
		commonwords = []
		for i in sentencea:
			if i in sentenceb and i not in commonwords:
				commonwords.append(i)
		


if __name__ == '__main__':
	sentence = sys.stdin.readline()
	sentence = listify(sentence)
	print response(sentence)

