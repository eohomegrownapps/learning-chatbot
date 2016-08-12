import respond
from dbutils import store
import random

class Chatbot:

	def __init__(self):
		self.filecorpus = "chatbot/logic/CommonWordsResponder/db/corpus.pkl"
		self.filedict = "chatbot/logic/CommonWordsResponder/db/dict.pkl"
		self.filestatements = "chatbot/logic/CommonWordsResponder/db/statements.pkl"

		corparr = store.unpickle(self.filecorpus)
		if corparr != False:
			#print "Loaded"
			self.lastid = corparr[2]
			self.corpus = corparr[0]
			self.fullcorp = corparr[1]
		else:
			#print "Initialising"
			self.corpus = [[["hello"],["hi"],0],[["hi"],["hello"],1]]
			self.lastid = 1
			self.fullcorp = {0:["Hello","Hi"],1:["Hi","Hello"]}


		dictarr = store.unpickle(self.filedict)
		if dictarr != False:
			self.dictionary = dictarr[0]
		else:
			self.dictionary = [["hello",2],["hi",2]]

		statearr = store.unpickle(self.filestatements)
		if statearr != False:
			self.statements = statearr[0]
			self.fullstate = statearr[2]
			self.laststateid = statearr[1]
		else:
			self.statements = []
			self.fullstate = {} 
			self.laststateid = -1
		random.seed()
		self.usestatement = 'False'
		#this would be statement id if true
		self.responder = respond.Responder(self.corpus,self.dictionary)
		self.count = 0
		self.threshold = 0.4

	def dictadd(self,sentencelist):
		for i in sentencelist:
			pointer = False
			for j in range(0,len(self.responder.dictionary)):
				if self.responder.dictionary[j][0] == i:
					self.responder.dictionary[j][1] += 1
					pointer = True
			if pointer == False:
				self.responder.dictionary.append([i,1])
			else:
				pointer = False

	def findindexbyid(self,sid):
		for i in range(0,len(self.statements)):
			if self.statements[i][1] == sid:
				return i

	def respondwithrate(self,sentence,answer):
		index = 0
		if len(answer) > 1:
			#higher frequency of words in answer (in dict) - more common words means more likely to be a 'catch-all' answer.
			arr = []
			for i in range(0,len(answer)):
				arr.append(self.responder.howcommon(answer[i][0]))
			maximum = 0
			for j in range(0, len(arr)):
				if arr[j]>arr[maximum]:
					maximum = j
			index = maximum


		rating = self.responder.rate(sentence, answer[index][0])
		#print rating
		#print answer
		if rating > 0.4:
			sentid = answer[0][2]
			return self.fullcorp[sentid][1]
		else:
			return False

	def reply(self,sentenceoriginal):
		sentenceoriginal = sentenceoriginal.rstrip()
		sentence = self.responder.listify(sentenceoriginal)
		finalanswer = ""
		if self.usestatement != 'False':
			#print "Using statement"
			self.lastid += 1
			#print "add to corpus"
			#print [statements[findindexbyid(usestatement)], sentence, lastid]
			#print [fullstate[usestatement],sentenceoriginal]
			self.responder.corpus.append([self.statements[self.findindexbyid(self.usestatement)][0], sentence, self.lastid])
			self.fullcorp[self.lastid] = [self.fullstate[self.usestatement],sentenceoriginal]
			self.dictadd(self.statements[self.findindexbyid(self.usestatement)][0])
			self.dictadd(sentence)

			for i in range(0,len(self.statements)):
				#print statements
				#print i
				#print fullstate
				if self.statements[i][1] == self.usestatement:
					#print "pop"
					#print statements[i]
					#print fullstate[findindexbyid(i)]
					self.fullstate.pop(self.usestatement)
					self.statements.pop(i)
					
					break
			#print "after pop"
			#print statements
			self.usestatement = 'False'
	
		answer = self.responder.response(sentence)
		if answer == False: 
			rating = 0
			if len(self.statements)>1:
				self.usestatement = self.statements[0][1]
				finalanswer = self.fullstate[self.usestatement]
			else:
				#for now choose random from corpus
				randomnum = random.randint(0,len(self.responder.corpus)-1)
				sentid = self.responder.corpus[randomnum][2]
				finalanswer = self.fullcorp[sentid][1]
		else:
			index = 0
			if len(answer) > 1:
				#higher frequency of words in answer (in dict) - more common words means more likely to be a 'catch-all' answer.
				arr = []
				for i in range(0,len(answer)):
					arr.append(self.responder.howcommon(answer[i][0]))
				maximum = 0
				for j in range(0, len(arr)):
					if arr[j]>arr[maximum]:
						maximum = j
				index = maximum


			rating = self.responder.rate(sentence, answer[index][0])
			if rating > self.threshold:
				sentid = answer[0][2]
				finalanswer = self.fullcorp[sentid][1]
			else:
				testsentence = self.responder.responserate(sentence)
				test = self.respondwithrate(sentence,testsentence)
				if test == False:
					#do the choose from statements thing
					#what to do if no statements?
					if len(self.statements)>1:
						#print statements
						#print fullstate
						self.usestatement = self.statements[0][1]
						finalanswer = self.fullstate[self.usestatement]
					else:
						#just give the answer returned.
						sentid = answer[0][2]
						finalanswer = self.fullcorp[sentid][1]
				else:
					finalanswer = test

		#add sentence to statements - check if it is already in statements 
		addstate = "true"
		for state in range(0,len(self.statements)):
			#print "---"
			#print statements[state][0]
			#print sentence
			if self.statements[state][0] == sentence:
				#print "same"
				addstate = state
				#print addstate
		#print addstate
		#TODO: Work on having many answers for 1 Q in corpus (e.g. ["How are you",["I'm fine","Not that great"]])

		#beginif
		if self.responder.sentenceincorpus(sentence)==False:
			if addstate == "true":
				#print "addtostatement"
				self.laststateid += 1
				addtostatement = [sentence,self.laststateid,rating]
				#print addtostatement
				addtofullstate = sentenceoriginal
				self.statements.append(addtostatement)
				self.fullstate[self.laststateid] = sentenceoriginal
			elif rating>self.statements[addstate][2]:
				self.statements[addstate][2] = rating

			if self.count%4==0:
				self.statements = sorted(self.statements, key=lambda x: x[2], reverse=True)
			else:
				self.statements = sorted(self.statements, key=lambda x: x[2])
			self.count+=1
		#endif
		return finalanswer

		#then add to corpus [comp statement, human statement] if not first
		#actually, maybe not
	def quit(self):
		print "Saving corpus..."
		picklecorpus = []
		picklecorpus.append(self.responder.corpus)
		picklecorpus.append(self.fullcorp)
		picklecorpus.append(self.lastid)
		store.pickle(self.filecorpus,picklecorpus)
		print "Saved"
		print "Saving dict..."
		pickledict = []
		pickledict.append(self.responder.dictionary)
		store.pickle(self.filedict,pickledict)
		print "Saved"
		print "Saving statements..."
		picklestate = []
		picklestate.append(self.statements)
		picklestate.append(self.laststateid)
		picklestate.append(self.fullstate)
		store.pickle(self.filestatements,picklestate)
		print "Saved"
		print "Goodbye"