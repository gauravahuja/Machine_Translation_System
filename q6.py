from math import log
from corpus import *
import sys

ibmm2tFileName = 'ibmm2t.dat'
ibmm2qFileName = 'ibmm2q.dat'
fc = 'original.de'
ec = 'scrambled.en'
unscrambledFile = 'unscrambled.en'

def getAlignments_3(fk, ek, t, q):
	A = []
	mk = len(fk)
	lk = len(ek) - 1
	for i in range(1, mk+1):
		fw = fk[i-1]
		maxV = 0
		maxA = 0
		for j in range(lk + 1):
			ew = ek[j]
			if q[(j, i, lk, mk)] > 0 and t.has_key(ew) and t[ew].has_key(fw):
				V = q[(j, i, lk, mk)]*t[ew][fw]
			else:
				V = largeNegConstant
			if (V > maxV):
				maxV = V
				maxA = j
		A.append(maxA)
	return A


def P(fk, ek, t, q):
	mk = len(fk)
	lk = len(ek) - 1
	a = getAlignments_3(fk, ek, t, q)
	p = 0
	assert(len(fk) == len(a))
	for i in range(len(fk)):
		fw = fk[i]
		ew = ek[a[i]]
		if q[(a[i], i, lk, mk)] > 1e-250 and t.has_key(ew) and t[ew].has_key(fw):
			try:
				p = p + log(q[(a[i], i, lk, mk)]*t[ew][fw])
			except ValueError:
				print "********Value Error**********"
				print (a[i], i, lk, mk)
				print ew
				print fw
				print q[(a[i], i, lk, mk)]
				print t[ew][fw]
				print "******************************"
				p = p + largeNegConstant
		else:
			p = p + largeNegConstant
			#print (a[i], i, lk, mk)
			#print ew
			#print fw
			#print q[(a[i], i, lk, mk)]
			#print t.has_key(ew)
			#print t[ew].has_key(fw)
			#print "******************"
	return p

def unscramble(fs, es, t, q):
	f = open(unscrambledFile, 'w')
	for k in range(len(fs)):
		fk = fs[k]
		maxEj = -1
		maxP = 0
		for j in range(len(es)):
			ej = es[j]
			p = P(fk, ej, t, q)	
			if j == 0:
				maxP = p
				maxEj = j
			elif p > maxP:
				maxP = p
				maxEj = j
		#end for j
		if k != 0:
			f.write('\n')
		f.write(' '.join(es[maxEj][1:]))
	#end for k
	f.close()
	
if __name__ == '__main__':
	t = loadP(ibmm2tFileName)
	q = loadP(ibmm2qFileName)
	(fs, es) = extractSentencesTxt(fc, ec)
	#print len(fs)
	#print len(es)
	#print fs[:10]
	#print es[:10]
	unscramble(fs, es, t, q)
