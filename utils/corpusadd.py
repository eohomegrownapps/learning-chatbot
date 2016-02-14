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
	arr = []
	speechold = sys.stdin.readline()
	while True:
		speech = sys.stdin.readline()
		arr.append(convert(speechold, speech))
		speechold = speech
		print arr