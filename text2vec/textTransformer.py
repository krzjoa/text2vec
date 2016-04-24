# coding=utf-8

import string
import tools as t
import string
import correct as c
import morfologik as m

class TextTransformer:
    def __init__(self):
        self.morfo = m.Morfo()
        self.c = c.Correct()
            
    def transform(self,rawDocuments):
        allPostags = []
        allUnknown = []
        allLemmas = []
        allMarkers = []
        documents = [self._preprocess(i) for i in rawDocuments]
        for j, k in zip(documents, rawDocuments):
            postags, unknown, lemmas = self.morfo.lemmPostag(j)
            allPostags.append(postags)
            allUnknown.append(unknown)
            allLemmas.append(lemmas)
            allMarkers.append(self._getMarkers(k.encode('utf-8')))
        return allPostags, allUnknown, allLemmas, allMarkers
    
   
    def _getMarkers(self,text):
        """ Kolejno: liczba wielokropków, uppercase'ów, ciągów ??!!!??? oraz ciągi w cudzysłowie"""
        markers = [0,0,0,0]
        markers[0]= t.countDotted(text)
        markers[1] = t.countEmot(text)
        markers[2] = t.countUpper(text)
        markers[3] = t.countQuot(text)
        return markers
        
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
        newUnknown = []
        emendationLogs = []
        for index, word in enumerate(unknown):
            corrected = self.c.correct(word.encode('utf-8'))
            print word, corrected
            if corrected != '_UNK_':
                postag, lemma, unk = self.morfo.lemmPostag(corrected)
                emendationLogs.append((word,corrected))
                if len(postag)>0:
                    newPostags[newPostags.index('_UNK_')] = postag
                    newLemmas[newLemmas.index('_UNK_')] = lemma
            else:
			   newUnknown.append(word)           
        return newPostags, newUnknown, newLemmas, emendationLogs
        
    def _preprocess(self,text):
		i = text.encode('utf').lower()
		i = i.replace("."," ").translate(string.maketrans("",""), string.punctuation)
		return i   
		


        
		 
		    
