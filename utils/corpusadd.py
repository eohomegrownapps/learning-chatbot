import sys
alphabet = "abcdefghijklmnopqrstuvwxyz"
def convert(sentence, response):
	sentence = listify(sentence)
	response = listify(response)
	sentence.pop(0)
	response.pop(0)
	return [sentence,response]
def listify(sentence):
	sentence = list(sentence.lower())
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
	return result

if __name__ == '__main__':
	filecorpus = "db/corpus.pkl"
	filedict = "db/dict.pkl"
	try:
		corparr = store.unpickle(filecorpus)
		lastid = corparr[1]
		corpus = corparr[0]
		dictarr= store.unpickle(filedict)
		dictionary = dictarr
	except IOError:
		corpus = []
		dictionary = []
		lastid = -1
		arr = []
	num = int(sys.stdin.readline())
	speecharr = []
	speechold = sys.stdin.readline()
	speecharr.append(speechold)
	for i in range(0,num-2)
		speech = sys.stdin.readline()
		speecharr.append(speech)
		speecharr.append(speech)
	speecharr.append(sys.stdin.readline())