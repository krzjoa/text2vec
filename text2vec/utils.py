# -*- coding: utf-8 -*-
import nltk
from nltk.util import ngrams
import cPickle as pickle
from random import shuffle


def getNgrams(words, min=1, max=4):
    s = []
    for n in range(min, max):
        for ngram in ngrams(words, n):
            s.append(' '.join(i.encode('utf-8') for i in ngram))
    return s
       
def shuffleData(x,y):
	xNew = []
	yNew = []
	index_shuf = range(len(x))
	shuffle(index_shuf)
	for i in index_shuf:
		xNew.append(x[i])
		yNew.append(y[i])   
	return xNew, yNew	 
	
def transformY(yInput, switch):
	Ytransformed = []
	for i in yInput:
		Ytransformed.append([switch[i]])
	return Ytransformed
    
    
def serialize(data, filename='data.pkl'):
	output = open(filename, 'wb')
	pickle.dump(data, output)
	output.close()

def deserialize(filename):
	pkl_file = open(filename, 'rb')
	data = pickle.load(pkl_file)
	pkl_file.close()
	return data
		
	    
