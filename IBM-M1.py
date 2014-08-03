"""
	author: Gaurav Ahuja
	date: November 14, 2013
	
	IBM Model 1
"""
import time
import sys
import cPickle as pickle
from collections import defaultdict
from corpus import *

ibmm1FileName = 'ibmm1.dat'

def calcDenominator(fs, es, t):
	d = defaultdict(float)	
	n = len(fs)
	for k in range(n):
		mk = len(fs[k])
		lk = len(es[k]) - 1 #Null word is included hence -1
		for i in range(1, mk+1): # fs[k][i-1] always
			fw = fs[k][i-1]
			for j in range(lk+1): # es[k][j] always
				ew = es[k][j]
				d[(k, i)] = d[(k, i)] + t[ew][fw] 
			#end for j
		#end for i
	#end for k
	return d

def updateT(t, wnc, wdc):
	ef = wnc.keys()
	for (ew, fw) in ef:
		t[ew][fw] = wnc[(ew, fw)]/wdc[ew]

def updateQ(q, pnc, pdc):
	p = pnc.keys()
	for (j, i, lk, mk) in p:
		q[(j, i, lk, mk)] = pnc[(j, i, lk, mk)]/pdc[(i, lk, mk)]

def IBM_M1(fs, es, S = 5):
	t = initializeT(fs, es)
	n = len(fs)
	for s in range(1, S+1):
		print "Iteration # %d" %(s)
		t1 = time.time()
		wnc = defaultdict(float)
		wdc = defaultdict(float)
		pnc = defaultdict(float)
		pdc = defaultdict(float)
		d = calcDenominator(fs, es, t)
		for k in range(n):
			mk = len(fs[k])
			lk = len(es[k]) - 1 #Null word is included hence -1
			for i in range(1, mk+1): # fs[k][i-1] always
				for j in range(lk+1): # es[k][j] always
					fw = fs[k][i-1]
					ew = es[k][j]
					
					delta = t[ew][fw]/d[(k, i)]
					
					wnc[(ew, fw)]		= wnc[(ew, fw)] + delta
					wdc[ew]				= wdc[ew] + delta
					pnc[(j, i, lk, mk)]	= pnc[(j, i, lk, mk)] + delta
					pdc[(i, lk, mk)]	= pdc[(i, lk, mk)] + delta
				#end for j
			#end for i
		#end for k
		updateT(t, wnc, wdc)
		t1 = time.time() - t1
		print "Time taken to complete iteration# %d: %.2f(s)" %(s, t1)
	#end for s	
	writeP(t, ibmm1FileName)		
	return t
	
if __name__ == '__main__':
	if(len(sys.argv) != 3):
		print "Usage: python IBM-M1.py foreignCorus.gz englishCorpus.gz"
		sys.exit(0)
	t1 = time.time()	
	(fs, es) = extractSentences(sys.argv[1], sys.argv[2])
	t = IBM_M1(fs, es)
	t1 = time.time()-t1
	print "Time taken to calculate IBM-M1: %.2f(s)" %(t1)
	
