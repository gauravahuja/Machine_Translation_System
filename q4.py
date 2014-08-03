import cPickle as pickle
from corpus import *

ibmm1FileName = 'ibmm1.dat'

devWordsFile = 'devwords.txt'
fc = 'corpus.de.gz'
ec = 'corpus.en.gz'

alignmentout = 'out-q4-alignment_model1.txt'
model1_out = 'out-q4-t_model1.txt'

def getAlignments_1(fk, ek, t):
	A = []
	for fw in fk:
		maxV = 0
		maxA = 0
		for i in range(len(ek)):
			ew = ek[i]
			V = t[ew][fw]
			if (V > maxV):
				maxV = V
				maxA = i
		#print (fw, ek[maxA], maxA)
		A.append(maxA)
	return A

t = loadP(ibmm1FileName)


f = open(devWordsFile, 'r')
words = f.readlines()
f.close()
	
f = open(model1_out, 'w')
i = 0
for word in words:
	word = word.strip()
	ft = sorted(t[word].items(), key = lambda x: x[1], reverse = True)
	if(i != 0):
		#print ""
		f.write("\n\n")
	i = 1
	#print word
	f.write(word+'\n')
	#print ft[:10]
	f.write(str(ft[:10]))
f.close()

			
(fs, es) = extractSentences(fc, ec)
fs = fs[:20]
es = es[:20]
f = open(alignmentout, 'w')
i = 0
for i in range(len(fs)):
	A = getAlignments_1(fs[i], es[i], t)
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
