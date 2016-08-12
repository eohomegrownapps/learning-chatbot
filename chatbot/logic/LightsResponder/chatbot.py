import respond
import sys
from dbutils import store
alphabet = "abcdefghijklmnopqrstuvwxyz"
class Chatbot:
	#corpus format: [["lights",val]...]
	def __init__(self):
		#self.filedict = "chatbot/logic/LightsResponder/db/dict.pkl"
		self.filedictfor = "db/dictfor.pkl"
		dictarrf = store.unpickle(self.filedictfor)
		if dictarrf != False:
			self.dictionaryf = dictarrf[0]
		else:
			self.dictionaryf = []
		self.filedictagainst = "db/dictagainst.pkl"
		dictarra = store.unpickle(self.filedictagainst)
		if dictarra != False:
			self.dictionarya = dictarra[0]
		else:
			self.dictionarya = []

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

	def respond(self, sentence):
		threshold = 0.2
		#return ["Answer", rating]
		lsentence = self.listify(sentence)
		bias = 0
		for i in lsentence:
			bias += self.calculateBias(i,True)
			bias -= self.calculateBias(i,False)
		return bias

	def calculateBias(self, word, isfor):
		occ = self.occurrences(word, isfor)
		if occ!=False:
			occ = float(occ[1])/float(self.sumdict(isfor))
			return occ
		else:
			return 0

	def occurrences(self, word, isfor):
		if isfor == True:
			d = self.dictionaryf
		else:
			d = self.dictionarya
		for index, i in enumerate(d):
			if i[0] == word:
				return [index, i[1]]
		return False

	def sumdict(self, isfor):
		if isfor == True:
			d = self.dictionaryf
		else:
			d = self.dictionarya
		s = 0
		for i in d:
			s += i[1]
		return s

	def addSentence(self, sentence, isLights):
		if isLights == True:
			d = self.dictionaryf
		else:
			d = self.dictionarya
		lsentence = self.listify(sentence)
		for i in lsentence:
			occ = self.occurrences(i,isLights)
			if occ != False:
				d[occ[0]][1]+=1
			else:
				d.append([i,1])

	def quit(self):
		print "Saving light for dict..."
		pickledictf = []
		pickledictf.append(self.dictionaryf)
		store.pickle(self.filedictfor,pickledictf)
		print "Saved"
		print "Saving light against dict..."
		pickledicta = []
		pickledicta.append(self.dictionarya)
		store.pickle(self.filedictagainst,pickledicta)
		print "Saved"
		print "Goodbye"

if __name__ == '__main__':
	c = Chatbot()
	while True:
		sentenceoriginal = sys.stdin.readline()
		sentenceoriginal = sentenceoriginal.rstrip()
		if sentenceoriginal == "quit":
			c.quit()
			break
		print c.respond(sentenceoriginal)
		v = sys.stdin.readline().rstrip()
		if v == 't':
			c.addSentence(sentenceoriginal,True)
		elif v == 'f':
			c.addSentence(sentenceoriginal,False)
		elif v == 'quit':
			c.quit()
			break
		print c.dictionaryf
		print c.dictionarya
