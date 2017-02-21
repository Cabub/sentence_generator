#!/usr/bin/python
#Caleb Eubanks
import sys
import nltk
import numpy
import os.path

def generate_sentence_with_ngrams(ngrams):
	db = {}
	for t in ngrams:
		if t in db.keys():
			v = db[t]
			db[t] = v + 1
		else:
			db[t] = 1
	sentence = ''
	lastwords = ('@',)
	lastword = ''
	n = 1
	for l in range(1000):
		matching = []
		for s in db.keys():
			temp = ()
			if len(s) <= len(lastwords):
				for i in range(len(s) - 1):
					temp += (lastwords[len(lastwords) - len(s) + 1 + i],)
				if tuple([s[i] for i in range(len(temp))]) == temp:
					matching += [s]
			else:
				for i in range(len(lastwords)):
					temp += (s[i],)
				if lastwords == temp:
					matching += [s]

		if len(matching) == 0:
			print('DEBUG: LASTWORDS = ' + str(lastwords))
			break
		total = sum([db[b] for b in matching])
		items = [b[n] if len(b) > n else b[len(b) - 1] for b in matching]
		probs = [numpy.double(db[b]) / total for b in matching]
		lastword = numpy.random.choice(items, p=probs)
		if lastword == '$':
			break
		if lastword in ['.', '?', '!', ';', ',']:
			sentence = sentence.strip() + lastword + ' '
		else:
			sentence += lastword + ' '
		lastwords += (lastword,)
		n += 1
	return sentence

def sentence_ngrams(text, n):
	sents = nltk.sent_tokenize(text)
	for i in range(len(sents)):
		sents[i] = '@ ' + sents[i] + ' $'
	text = (' '.join(sents)).replace('\n', ' ')
	ngrams = []
	for sent in sents:
		for gram in nltk.ngrams(nltk.word_tokenize(sent), n):
			ngrams += [gram]
	return ngrams

def generate_n_sentences(n, ngrams):
	output = ''
	for i in range(n):
		output += generate_sentence_with_ngrams(ngrams)
	return output

def print_help():
	print("generate_n_sentences <number of sentences> [<filename>]")
	print("generates sentences based on bigrams, trigrams, and quadgrams")
	print("you can also pass text through stdin, like cat book.txt | generate_n_sentences 5")

try:
	n = int(sys.argv[1])
	if len(sys.argv) > 2:
		file = open(sys.argv[2])
		corpus = file.read()
		file.close()
	else:
		corpus = sys.stdin.read()

#	bigrams = sentence_ngrams(corpus,2)
	trigrams = sentence_ngrams(corpus,3)
	quadgrams = sentence_ngrams(corpus,4)

#	ngrams = bigrams + trigrams # + quadgrams
	ngrams = trigrams + quadgrams
	
	print(generate_n_sentences(n, ngrams))
except:
	print_help()
	sys.exit()


		
	

