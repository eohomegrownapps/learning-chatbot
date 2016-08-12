import sys
corpus = [[["do","you","like","fish"],["yes","i","like","fish"]], [["i","hate","potatoes"],["no","i","dont"]],[["i", "have", "to", "go", "to", "the", "bathroom"], ["you", "drink", "too", "much", "coffee"]], [["you", "drink", "too", "much", "coffee"], ["but", "i", "love", "coffee"]], [["but", "i", "love", "coffee"], ["well", "its", "your", "life"]], [["well", "its", "your", "life"], ["you", "eat", "too", "much", "chocolate"]], [["you", "eat", "too", "much", "chocolate"], ["i", "dont", "think", "so"]], [["i", "dont", "think", "so"], ["have", "you", "looked", "in", "the", "mirror"]], [["have", "you", "looked", "in", "the", "mirror"], ["do", "you", "think", "im", "getting", "fat"]], [["do", "you", "think", "im", "getting", "fat"], ["i", "didnt", "say", "that"]], [["i", "didnt", "say", "that"], ["what", "did", "you", "say"]], [["what", "did", "you", "say"], ["i", "said", "i", "have", "to", "go", "to", "the", "bathroom"]]]
#stored as words in array
#olddict: dictionary = [["do",1],["you",1],["like",2],["fish",2],["yes",1],["i",3],["hate",1],["potatoes",1],["no",1],["dont",1]]
dictionary = [['do', 1], ['you', 11], ['like', 2], ['fish', 2], ['yes', 1], ['i', 12], ['hate', 1], ['potatoes', 1], ['no', 1], ['dont', 3], ['have', 4], ['to', 4], ['go', 2], ['the', 4], ['bathroom', 2], ['drink', 2], ['too', 4], ['much', 4], ['coffee', 4], ['but', 2], ['love', 2], ['well', 2], ['its', 2], ['your', 2], ['life', 2], ['eat', 2], ['chocolate', 2], ['think', 4], ['so', 2], ['looked', 2], ['in', 2], ['mirror', 2], ['do', 1], ['im', 2], ['getting', 2], ['fat', 2], ['do', 1], ['didnt', 2], ['say', 4], ['that', 2], ['what', 2], ['did', 2], ['said', 1]]
alphabet = "abcdefghijklmnopqrstuvwxyz"
def response(sentence):
	sentencesort = []
	for i in range(0,len(sentence)):
		commonval = 0
		dictentry = searchdict(sentence[i])
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
	return common(sentencesortnew,corpus)

def common(s, corpu):
	#print s
	#returns corpus consisting of [["statement"],["response"]]
	if len(corpu) == 1:
		return corpu
	if len(s) == 0:
		if len(corpu) > 0:
			return corpu
		else:
			return None
	if searchdict(s[0]) != False:
		corpu = searchcorpus(s[0],corpu)
		#print corpu
	s.pop(0)
	return common(s, corpu)

def listify(sentence):
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

def searchdict(word):
	for i in dictionary:
		if word == i[0]:
			return i[1]
	return False

#def searchsentences(word, sentences):
#	for i in sentences:
#		if word in 

def searchcorpus(word, corp):
	result = []
	for i in corp:
		stripped = i[0]
		if word in stripped:
			result.append(i)
	return result

if __name__ == '__main__':
	sentence = sys.stdin.readline()
	sentence = listify(sentence)
	print response(sentence)

