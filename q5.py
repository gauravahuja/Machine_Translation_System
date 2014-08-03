import cPickle as pickle
from corpus import *

ibmm1FileName = 'ibmm1.dat'
ibmm2tFileName = 'ibmm2t.dat'
ibmm2qFileName = 'ibmm2q.dat'

fc = 'corpus.de.gz'
ec = 'corpus.en.gz'

alignmentout = 'out-q5-alignment_model2.txt'

def getAlignments_2(fk, ek, t, q):
	A = []
	mk = len(fk)
	lk = len(ek) - 1
	for i in range(1, mk+1):
		fw = fk[i-1]
		maxV = 0
		maxA = 0
		for j in range(lk + 1):
			ew = ek[j]
			V = q[(j, i, lk, mk)]*t[ew][fw]
			if (V > maxV):
				maxV = V
				maxA = j
		A.append(maxA)
	return A

t = loadP(ibmm2tFileName)
q = loadP(ibmm2qFileName)

			
(fs, es) = extractSentences(fc, ec)
fs = fs[:20]
es = es[:20]
f = open(alignmentout, 'w')
i = 0
for i in range(len(fs)):
	A = getAlignments_2(fs[i], es[i], t, q)
	fss = ' '.join(fs[i])
	ess = ' '.join(es[i][1:])
	if (i!= 0):
		#print ""
		f.write('\n\n')
	i = 1
	#print ess
	f.write(ess+'\n')
	#print fss + "\n"
	f.write(fss+'\n')
	#print A
	f.write(str(A))
f.close()
