# coding=utf-8
from pyMorfologik import Morfologik
from pyMorfologik.parsing import ListParser

        
class Morfo:
    def __init__(self):
        self.parser = ListParser()
        self.stemmer = Morfologik() 
        
    def lemmPostag(self,text):
		transformed = self._getTransformed(text)
		postags = []
		lemmas = []
		unknown = []
		for i in transformed:
			x = i[1].values()
			z = i[1].keys()
			if len(x)>0:
				postags.append(x[-1][0])
				lemmas.append(z[-1])
			else:
				postags.append('_UNK_')
				lemmas.append('_UNK_')
				unknown.append(i[0])
		return postags, unknown, lemmas
    
    def _getTransformed(self,text):
        return self.stemmer.stem([text],self.parser)
