# -*- coding: utf-8 -*-

#A little message: "You absolutely do NOT let an algorithm mindlessly devour a whole bunch of data that you haven't vetted even a little bit."

import sys
from chatbot.logic.CommonWordsResponder import chatbot as CommonWordsResponder
import datetime

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

#TODO: If respond fails (goes to statement), try a 'rate respond'. If this is over the threshold, give it.

print r""" 
 ___       _______   ________  ________  ________   ___  ________   ________     
|\  \     |\  ___ \ |\   __  \|\   __  \|\   ___  \|\  \|\   ___  \|\   ____\    
\ \  \    \ \   __/|\ \  \|\  \ \  \|\  \ \  \\ \  \ \  \ \  \\ \  \ \  \___|    
 \ \  \    \ \  \_|/_\ \   __  \ \   _  _\ \  \\ \  \ \  \ \  \\ \  \ \  \  ___  
  \ \  \____\ \  \_|\ \ \  \ \  \ \  \\  \\ \  \\ \  \ \  \ \  \\ \  \ \  \|\  \ 
   \ \_______\ \_______\ \__\ \__\ \__\\ _\\ \__\\ \__\ \__\ \__\\ \__\ \_______\
    \|_______|\|_______|\|__|\|__|\|__|\|__|\|__| \|__|\|__|\|__| \|__|\|_______|
                                                                                 
                                                                                 
 ________  ___  ___  ________  _________  ________  ________  _________          
|\   ____\|\  \|\  \|\   __  \|\___   ___\\   __  \|\   __  \|\___   ___\        
\ \  \___|\ \  \\\  \ \  \|\  \|___ \  \_\ \  \|\ /\ \  \|\  \|___ \  \_|        
 \ \  \    \ \   __  \ \   __  \   \ \  \ \ \   __  \ \  \\\  \   \ \  \         
  \ \  \____\ \  \ \  \ \  \ \  \   \ \  \ \ \  \|\  \ \  \\\  \   \ \  \        
   \ \_______\ \__\ \__\ \__\ \__\   \ \__\ \ \_______\ \_______\   \ \__\       
    \|_______|\|__|\|__|\|__|\|__|    \|__|  \|_______|\|_______|    \|__|       
                                                                                 
© Euan Ong 2016 http://homegrownapps.tk

Hi, user.
Talk to me; help me learn."""

sys.stdout.write("> ")
chat = CommonWordsResponder.Chatbot()
directory = "logs"
logname = directory+"/"+"{:%Y-%m-%d-%H:%M}_chat.log".format(datetime.datetime.now())
while True:
	#print corpus
	#print dictionary
	sentenceoriginal = sys.stdin.readline()
	#pdb.set_trace()
	sentenceoriginal = sentenceoriginal.rstrip()
	sentence = chat.responder.listify(sentenceoriginal)
	if len(sentence)>0 and sentence[0] == "quit":
		chat.quit()
		break
	r = chat.reply(sentenceoriginal)	
	print r
	sys.stdout.write("> ")

	with open(logname,'a') as file:
		file.write("User:    "+sentenceoriginal+"\n")
		file.write("Chatbot: "+r+"\n")
