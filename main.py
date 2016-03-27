from chatbot import respond
from dbutils import store
import sys
import random

#corpus = [[["do","you","like","fish"],["yes","i","like","fish"]], [["i","hate","potatoes"],["no","i","dont"]],[["i", "have", "to", "go", "to", "the", "bathroom"], ["you", "drink", "too", "much", "coffee"]], [["you", "drink", "too", "much", "coffee"], ["but", "i", "love", "coffee"]], [["but", "i", "love", "coffee"], ["well", "its", "your", "life"]], [["well", "its", "your", "life"], ["you", "eat", "too", "much", "chocolate"]], [["you", "eat", "too", "much", "chocolate"], ["i", "dont", "think", "so"]], [["i", "dont", "think", "so"], ["have", "you", "looked", "in", "the", "mirror"]], [["have", "you", "looked", "in", "the", "mirror"], ["do", "you", "think", "im", "getting", "fat"]], [["do", "you", "think", "im", "getting", "fat"], ["i", "didnt", "say", "that"]], [["i", "didnt", "say", "that"], ["what", "did", "you", "say"]], [["what", "did", "you", "say"], ["i", "said", "i", "have", "to", "go", "to", "the", "bathroom"]]]
#stored as words in array
#corpus [[[a],[b],[id]],[[c],[d],[id]]]
#fullcorp {0:["Hello","Hi"],1:["Hi","Hello"]}
#olddict: dictionary = [["do",1],["you",1],["like",2],["fish",2],["yes",1],["i",3],["hate",1],["potatoes",1],["no",1],["dont",1]]
#dictionary = [['do', 1], ['you', 11], ['like', 2], ['fish', 2], ['yes', 1], ['i', 12], ['hate', 1], ['potatoes', 1], ['no', 1], ['dont', 3], ['have', 4], ['to', 4], ['go', 2], ['the', 4], ['bathroom', 2], ['drink', 2], ['too', 4], ['much', 4], ['coffee', 4], ['but', 2], ['love', 2], ['well', 2], ['its', 2], ['your', 2], ['life', 2], ['eat', 2], ['chocolate', 2], ['think', 4], ['so', 2], ['looked', 2], ['in', 2], ['mirror', 2], ['do', 1], ['im', 2], ['getting', 2], ['fat', 2], ['do', 1], ['didnt', 2], ['say', 4], ['that', 2], ['what', 2], ['did', 2], ['said', 1]]
#filecorpus: [corpus,lastid (this is last id used),corpfull]
#filedict: [dictarr]
#filestatements: [statements, laststateid,fullstate]
#statements: [[["a","human","statement"],0,rateval],[["another","human","statement"],1,rateval]] in order of rateval - lowest first.
#fullstatements: {0:"A human statement",1:"Another human statement"}
#These are responses to questions human has said. 
#if a statement == a str in corpus, it can be removed along with its corresponding dict pair

#on computer response: look for statement matching it.

#TODO: develop algorithm for qualitative comparison of input to corpus probs
#Test algorithm:
#for every common word, sum of frequencies of words common to both sentences as fraction

#to be developed: 
#incorporate length difference of sentences; fraction of common words / ave length of sentences
#context (last sentence) - how common is the context of the 'q' part of sentence that will be used to the current sentence? 
#run rate() on all possible contexts for a sentence and then take the best result.
#etc. NN implementation would really be useful

#with algorithm, run it on (sentence, response). if rate > 0.5 (just test value, can be improved with trials or a NN):
#just give response
#otherwise respond by saying the first statement in statements (i.e. lowest rate value)
#give rate trigger value (called threshold) as storage in database
threshold = 0.5


def quit():
	print "Saving corpus..."
	picklecorpus = []
	picklecorpus.append(corpus)
	picklecorpus.append(fullcorp)
	picklecorpus.append(lastid)
	store.pickle(filecorpus,picklecorpus)
	print "Saved"
	print "Saving dict..."
	pickledict = []
	pickledict.append(dictionary)
	store.pickle(filedict,pickledict)
	print "Saved"
	print "Goodbye"

def dictadd(sentencelist, respondinst):
	for i in sentencelist:
		if respondinst.searchdict(i)


#CONFIG
filecorpus = "db/corpus.pkl"
filedict = "db/dict.pkl"
filestatements = "db/statements.pkl"

corparr = store.unpickle(filecorpus)
if corparr != False:
	lastid = corparr[2]
	corpus = corparr[0]
	fullcorp = corparr[1]
else:
	corpus = [[["hello"],["hi"],0],[["hi"],["hello"],1]]
	lastid = 1
	fullcorp = {0:["Hello","Hi"],1:["Hi","Hello"]}


dictarr = store.unpickle(filedict)
if dictarr != False:
	dictionary = dictarr[0]
else:
	dictionary = [["hello",2],["hi",2]]

statearr = store.unpickle(filestatements)
if statearr != False:
	statements = statearr[0]
	fullstate = statearr[2]
	laststateid = statearr[1]
else:
	statements = []
	fullstate = {} 
	laststateid = -1
random.seed()
usestatement = False
#this would be statement id if true
responder = respond.Responder(corpus,dictionary)
while True:
	#print corpus
	#print dictionary
	sentenceoriginal = sys.stdin.readline()
	sentence = responder.listify(sentenceoriginal)
	if sentence[0] == "quit":
		quit()
		break
	if usestatement != False:
		lastid += 1
		corpus.append([statements[usestatement], sentence, lastid])
		fullstate[lastid] = [fullstate[usestatement],sentenceoriginal]
		for i in range(0,len(statements)):
			if statements[i][1] == usestatement:
				statements.pop(i)
				fullstate.pop(i)
		usestatement = False
		dictadd(statements[usestatement])
		dictadd(sentence)
	
	answer = responder.response(sentence)
	if answer == False: 
		rating = 0
		if len(statements)>1:
			usestatement = statements[0][1]
			returned = fullstate[usestatement]
			print returned
		else:
			#for now choose random from corpus
			randomnum = random.randint(0,len(corpus)-1)
			sentid = corpus[randomnum][2]
			print fullcorp[sentid][1]
	else:
		index = 0
		if len(answer) > 1:
			#higher frequency of words in answer (in dict) - more common words means more likely to be a 'catch-all' answer.
			arr = []
			for i in range(0,len(answer)):
				arr.append(responder.howcommon(answer[i][0]))
			maximum = 0
			for j in range(0, len(arr)):
				if arr[j]>arr[maximum]:
					maximum = j
			index = maximum


		rating = responder.rate(sentence, answer[index][0])
		if rating > 0.5:
			sentid = answer[0][2]
			print fullcorp[sentid][1]
		else:
			#do the choose from statements thing
			#what to do if no statements?
			if len(statements)>1:
				usestatement = statements[0][1]
				returned = fullstate[usestatement]
				print returned
			else:
				sentid = answer[0][2]
				print fullcorp[sentid][1]

	laststateid += 1
	addtostatement = [sentence,laststateid,rating]
	addtofullstate = sentenceoriginal
	statements.append(addtostatement)
	statements = sorted(statements, key=lambda x: x[2])
	fullstate[laststateid] = sentenceoriginal

	#then add to corpus [comp statement, human statement] if not first
	#actually, maybe not
