corpus = [[["do","you","like","fish"],["yes","i","like","fish"]], [["i","hate","potatoes"],["no","i","dont"]],[["i", "have", "to", "go", "to", "the", "bathroom"], ["you", "drink", "too", "much", "coffee"]], [["you", "drink", "too", "much", "coffee"], ["but", "i", "love", "coffee"]], [["but", "i", "love", "coffee"], ["well", "its", "your", "life"]], [["well", "its", "your", "life"], ["you", "eat", "too", "much", "chocolate"]], [["you", "eat", "too", "much", "chocolate"], ["i", "dont", "think", "so"]], [["i", "dont", "think", "so"], ["have", "you", "looked", "in", "the", "mirror"]], [["have", "you", "looked", "in", "the", "mirror"], ["do", "you", "think", "im", "getting", "fat"]], [["do", "you", "think", "im", "getting", "fat"], ["i", "didnt", "say", "that"]], [["i", "didnt", "say", "that"], ["what", "did", "you", "say"]], [["what", "did", "you", "say"], ["i", "said", "i", "have", "to", "go", "to", "the", "bathroom"]]]
dictionary =[]
def dictmake(corpus):
	for i in corpus:
		for k in i[0]:
			find = findindex(k,dictionary)
			if find != False:
				dictionary[find][1]+=1
			else:
				dictionary.append([k,1])
		for k in i[1]:
			find = findindex(k,dictionary)
			if find != False:
				dictionary[find][1]+=1
			else:
				dictionary.append([k,1])
	return dictionary
def findindex(word,source):
	for i in range(0,len(source)):
		if source[i][0] == word:
			return i
	return False

if __name__ == '__main__':
	print dictmake(corpus)