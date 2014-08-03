"""
	author: Gaurav Ahuja
	date: November 14, 2013
	
	Corpus reading functions
"""

import gzip
import time
import cPickle as pickle
from collections import defaultdict

nullWord = '__null__'
largeNegConstant = -800

def extractSentences(f,e):
	"""
	param f: Foreign/Source Language corpus in gzipped text format (.gz)
	param e: English/Target Language corpus in gzipped text format (.gz)
	f and e are gunzipped text files of the corpus.
	f and e contain parallel translations
	
	return: List of Foreign and English language sentences tokenized into words.
	Every English sentence starts with a nullWord.
	"""
	
	ff = gzip.open(f, 'r')
	fs = ff.readlines()
	ff.close()
	
	ef = gzip.open(e, 'r')
	es = ef.readlines()
	ef.close()
	
	assert(len(fs) == len(es))
	
	for i in range(len(fs)):
		fs[i] = fs[i].strip().split()
		es[i] = [nullWord] + es[i].strip().split()
	
	return (fs, es)
	
def extractSentencesTxt(f,e):
	"""
	param f: Foreign/Source Language corpus in .txt format
	param e: English/Target Language corpus in .txt format
	f and e are gunzipped text files of the corpus.
	f and e contain parallel translations
	
	return: List Foreign and English language sentences tokenized into words.
	Every English sentence starts with a nullWord.
	"""
	
	ff = open(f, 'r')
	fs = ff.readlines()
	ff.close()
	
	ef = open(e, 'r')
	es = ef.readlines()
	ef.close()
	
	
	for i in range(len(fs)):
		fs[i] = fs[i].strip().split()
	
	for i in range(len(es)):
		es[i] = [nullWord] + es[i].strip().split()
	
	return (fs, es)
	
def getEF(fs, es):
	e2f = defaultdict(set)
	f2e = defaultdict(set)
	for i in range(len(fs)):
		for fw in fs[i]:
			for ew in es[i]:
				e2f[ew].add(fw) 
				f2e[fw].add(ew)
	return (f2e, e2f)
	
def getNE(fs, es):
	(f2e, e2f) = getEF(fs, es)
	n = {}
	for ew in e2f.keys():
		n[ew] = float(len(e2f[ew]))
	return n
	
def initializeT(fs, es):
	t = {}
	n = getNE(fs, es)
	for i in range(len(fs)):
		for ew in es[i]:
			if t.has_key(ew) == False:
				t[ew] = {}	
			for fw in fs[i]:
				t[ew][fw] = 1/n[ew] 
	return t

def initializeQ(fs, es):
	q = defaultdict(float)
	n = len(fs)
	for k in range(n):
		mk = len(fs[k])
		lk = len(es[k]) - 1 #Null word is included hence -1
		for i in range(1, mk+1): # fs[k][i-1] always
			for j in range(lk+1): # es[k][j] always
				q[(j, i, lk, mk)] = 1/float(lk+1)
	return q
	
def loadP(fileName):
	f = open(fileName, 'r')
	p = pickle.load(f)
	f.close()
	return p
	
def writeP(p, fileName):
	f = open(fileName, 'w')
	pickle.dump(p, f, protocol=2)
	f.close()
		
	
if __name__ == '__main__':
	(fs, es) = extractSentences('corpus.de.gz', 'corpus.en.gz')
	print "Number of sentences: %d" %(len(fs))
	t1 = time.time()
	(f2e, e2f) = getEF(fs, es)
	t1 = time.time() - t1
	print "Time to getEF: %.2f(s)" %(t1)
	print "Number of unique foreign words: %d" %(len(f2e.keys()))
	print "Number of unique english words: %d + null word" %(len(e2f.keys())-1)
	n = getNE(fs, es)
	print "n[nullWord] = %d" %(n[nullWord])
	t1 = time.time()
	t =  initializeT(fs, es)
	t1 = time.time()-t1
	print "Time to initializeT: %.2f(s)" %(int(t1))
	print "t('sich'|nullWord) = %f" %(t[nullWord]['sich'])
