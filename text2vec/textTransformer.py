# coding=utf-8

import aspell
from pyMorfologik import Morfologik
from pyMorfologik.parsing import ListParser
import string
import tools as t

class Correct:
    def __init__(self):
        self.s = aspell.Speller(('lang','pl'),('master', '/home/krzysztof/Pulpit/Projekt/pl/pl.rws'))
        
    def correct(self,word):
        suggested = self.s.suggest(word)
        if len(suggested)>0:
            return suggested[0]
        else:
            return '_UNK_'
        
    def suggest(self, word):
        return self.s.suggest(word)

class TextTransformer:
    def __init__(self):
        self.parser = ListParser()
        self.stemmer = Morfologik()
        self.c = Correct()
     
    def transform(self,rawDocuments):
        allPostags = []
        allUnknown = []
        allLemmas = []
        allMarkers = []
        documents = [[i.encode('utf-8').lower()] for i in rawDocuments]
        for j in documents:
            postags, unknown, lemmas = self._transformDocument(j)
            allPostags.append(postags)
            allUnknown.append(unknown)
            allLemmas.append(lemmas)
            allMarkers.append(self._getMarkers(j[0]))
        return allPostags, allUnknown, allLemmas, allMarkers
    
    def _transformDocument(self,comment):
        postags = []
        unknown = []
        lemmas = []
        posTagLemm = self.stemmer.stem(comment,self.parser)
        for i in posTagLemm:
            x = i[1].values()
            z =i[1].keys()
            if len(x)>0:
                postags.append(x[0][0])
                lemmas.append(z[0])
            else:
                postags.append('_UNK_')
                lemmas.append('_UNK_')
                unknown.append(i[0])
        return postags, unknown, lemmas
    
    def _getMarkers(self,text):
        """ Kolejno: liczba wielokropków, uppercase'ów i ciągów ??!!!??? """
        markers = [0,0,0]
        markers[0]= t.countDotted(text)
        markers[1] = t.countEmot(text)
        markers[2] = t.countUpper(text)
        
    def autocorrect(self,documents):
		allLemmas = [document.lemmas for document in documents]
		allPostags = [document.postags for document in documents]
		allUnknown = [document.unknown for document in documents]
		newPostags = allPostags
		newUnknown = allUnknown
		newLemmas = allLemmas
		emendationLogs = [[] for i in documents]
		for pstg, unk, lemm, index in zip(allPostags, allUnknown, allLemmas, range(len(allPostags))):
			newPostags[index],newUnknown[index], newLemmas[index], emendationLogs[index] = self._docCorrect(pstg, unk, lemm)
		return newPostags, newUnknown, newLemmas, emendationLogs

    def _docCorrect(self, postags, unknown, lemmas):
        newLemmas = lemmas
        newPostags = postags
        newUnknown = unknown
        emendationLogs = []
        print lemmas, postags, unknown
        for index, word in enumerate(unknown):
            corrected = self.c.correct(word.encode('utf-8'))
            if corrected != '_UNK_':
                newPostag = self.stemmer.stem([corrected], self.parser)[0][1].values()
                newLemma = self.stemmer.stem([corrected], self.parser)[0][1].keys()
                print word, corrected
                emendationLogs.append((word,corrected))
                if len(newPostag)>0:
                    newPostags[newPostags.index('_UNK_')] = newPostag[0][0]
                    newLemmas[newLemmas.index('_UNK_')] = newLemma[0]
                    del newUnknown[index]
        print emendationLogs            
        return newPostags, newUnknown, newLemmas, emendationLogs
