# coding=utf-8

import tools as t

class TextTransformer:
    def __init__(self):
        self.parser = ListParser()
        self.stemmer = Morfologik()
        self.c = Correct()
     
    def transform(self,rawComments):
        allPostags = []
        allUnknown = []
        allLemmas = []
        allMarkers = []
        rawComms = [[i.encode('utf-8').lower()] for i in rawComments]
        for j in rawComms:
            postags, unknown, lemmas = self._transformComment(j)
            allPostags.append(postags)
            allUnknown.append(unknown)
            allLemmas.append(lemmas)
        return allPostags, allUnknown, allLemmas
    
    def _posTagLemm(self,comment):
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
