# coding=utf-8
from operator import add
from collections import Counter
import string
import tools as t
import cPickle as pickle
import textTransformer as tt
import utils as u

class Document:
    def __init__(self,original, label=''):
        self.label = label
        self.original = original
        self.tokenized = t.clean(self.original.split())
        self.lemmas = []
        self.unknown = []
        self.bilemmas = []
        self.postags = []
        self.bipostags = []
        self.markers = []
        self.emendationLogs = []
	
	def compute(self, bigrams=False):
		self.lemmas, self.unknownLemmas = t.lemmatize(self.tokenized)	
		self.postags , self.unknownPostags = t.pos(self.lemmas)
		if bigrams:
			self.bilemmas = u.getNgrams(self.lemmas, min=2, max=3)
			self.bipostags = u.getNgrams(self.postags, min=2, max=3)	
		
class TextModel:
	def __init__(self):
		self.documents = []
		self.lemmatizer = tt.TextTransformer()
		self.lemmasCount = dict()
		self.postagsCount = dict()
		self.unknownCount = dict()
		self.bilemmasCount = dict()
		self.bipostagsCount = dict()
		self.uniqueLemmas = []
		self.uniquePostags = []
		self.uniqueBilemmas = []
		self.uniqueBipostags = []
		self.isEmended = False
		self.isBigrams = False
		#~ self.lemmaNgrams = 0
		#~ self.postagsNgrams = 0
			
	def fit(self,documents, labels, autocorrect=False, bigrams=False):
		self.documents  = [Document(i, j) for i, j in  zip(documents, labels)]
		pos, unk, lem, mark  = self.lemmatizer.transform(documents)
		for p, u, l, m, document in zip(pos, unk, lem, mark, self.documents):
			document.lemmas = l
			document.postags = p
			document.unknown = u
			document.markers = m	
		if autocorrect: self.emend(bigrams=bigrams)
		if bigrams and not autocorrect: self._getBigrams()
		if not self.isEmended: self._computeVectorModel()					

	def _computeVectorModel(self, bigrams=False):			
		self.lemmasCount = dict(Counter(reduce(add,[document.lemmas for document in self.documents])))
		self.postagsCount = dict(Counter(reduce(add,[document.postags for document in self.documents])))
		self.unknownCount = dict(Counter(reduce(add,[document.unknown for document in self.documents])))
		self.uniqueLemmas = list(self.lemmasCount)
		self.uniquePostags = list(self.postagsCount)
		if bigrams:
			self.bilemmasCount = dict(Counter(reduce(add,[document.bilemmas for document in self.documents])))
			self.bipostagsCount = dict(Counter(reduce(add,[document.bipostags for document in self.documents])))
			self.uniqueBilemmas = list(self.bilemmasCount)
			self.uniqueBipostags = list(self.bipostagsCount)
			
	def _getBigrams(self):
		for document in self.documents:
			document.bilemmas = u.getNgrams(document.lemmas, min=2, max=3)
			document.bipostags = u.getNgrams(document.postags, min=2, max=3)
		self.isBigrams=True	
		
	def emend(self, bigrams=False):
		newPos, newUnk, newLem, emendationLogs = self.lemmatizer.autocorrect(self.documents)
		for l, p, u, eml, document in zip(newLem, newPos, newUnk, emendationLogs, self.documents):
			document.lemmas = l
			document.postags = p
			document.unknown = u
			document.emendationLogs=eml	
		self.isEmended = True
		if bigrams: self._getBigrams()	
		self._computeVectorModel()	
		
	# Get lemmas, postags, unknown, markers
		
	def getLemmas(self):
		return [document.lemmas for document in self.documents]	
		
	def getUniqueLemmas(self):
		return self.uniqueLemmas
	
	def getLemmasFreq(self):
		return sorted(self.lemmasCount.items(), key=lambda x:x[1], reverse=True)
	
	def totalLemmasCount(self):
		return sum(self.lemmasCount.values())	
				
	def getBilemmas(self):
		return [document.bilemmas for document in self.documents]	
		
	def getUniqueBilemmas(self):
		return self.uniqueBilemmas
	
	def getBilemmasFreq(self):
		return sorted(self.bilemmasCount.items(), key=lambda x:x[1], reverse=True)
	
	def totalBilemmasCount(self):
		return sum(self.bilemmasCount.values())			
		
	def getPostags(self):
		return [document.postags for document in self.documents]	
		
	def getUniquePostags(self):
		return self.uniquePostags
		
	def getPostagsFreq(self):
		return sorted(self.postagsCount.items(), key=lambda x:x[1], reverse=True)
		
	def totalPostagsCount(self):
		return sum(self.postagsCount.values())
								
	def getPostags(self):
		return [document.postags for document in self.documents]	
		
	def getUniquePostags(self):
		return self.uniquePostags
		
	def getPostagsFreq(self):
		return sorted(self.postagsCount.items(), key=lambda x:x[1], reverse=True)
		
	def totalPostagsCount(self):
		return sum(self.postagsCount.values())						
		
	def getUnknown(self):
		return [document.unknown for document in self.documents]
	
	def getUniqueUnknown(self):
		return set(reduce(add,self.getUnknown))	
		
	def getUnknownFreq(self):
		return sorted(self.unknownCount.items(), key=lambda x:x[1], reverse=True)	
		
	def totalUnknownCount(self):
		return sum(self.unknownCount.values())				
		
	def getEmendationLogs(self):
		return [document.emendationLogs for document in self.documents]
	
	def getAllEmendationLogs(self):
		return reduce(add,self.getEmendationLogs())			
		
	def getVectors(self):
		lemmasVecs =  [[document.lemmas.count(word) for word in self.uniqueLemmas] for document in self.documents]
		postagsVecs = [[document.postags.count(posTag) for posTag in self.uniquePostags] for document in self.documents]
		markersVecs = [document.markers for document in self.documents]
		x = [m + l + p for m, l, p in zip(markersVecs, lemmasVecs, postagsVecs)]
		y = [document.label for document in self.documents]
		if self.isBigrams:
			bilemmasVecs = [[document.bilemmas.count(word) for word in self.uniqueBilemmas] for document in self.documents]
			bipostagsVecs = [[document.bipostags.count(word) for word in self.uniqueBipostags] for document in self.documents]
			x = [vec + bl + bp for vec, bl, bp in zip(x,bilemmasVecs, bipostagsVecs)]
		return x, y
		
	def vectorize(self, text):
		document = Document(text)
		pos, unk, lem, mark = self.lemmatizer.transform([text])
		document.postags, document.unknown, document.lemmas, document.markers = pos[0], unk[0], lem[0], mark[0]
		lemmasVec =  [document.lemmas.count(word) for word in self.uniqueLemmas]	
		postagsVec =  [document.postags.count(posTag) for posTag in self.uniquePostags]
		bilemmasVec =  [document.bilemmas.count(word) for word in self.uniqueBilemmas]	
		bipostagsVec =  [document.bipostags.count(biposTag) for biposTag in self.uniqueBipostags]
		return 	document.markers + lemmasVec + postagsVec + bilemmasVec + bipostagsVec
			
	def devectorize(self, vector):
		lemmas = []
		postags = []
		markers = []
		bilemmas = []
		bipostags = []
		
		"""1st part: markers"""
		markers = vector[:3]	
		"""2nd part: lemmas """
		for index, value in enumerate(vector[3:][:len(self.uniqueLemmas)]):
			for j in range(value):
				lemmas.append(self.uniqueLemmas[index])
		"""3rd part: postags """		
		for index, value in enumerate(vector[3:][len(self.uniqueLemmas):][:len(self.uniquePostags)]):
			for j in range(value):
				postags.append(self.uniquePostags[index])		
		"""4th part: bilemmas"""
		for index, value in enumerate(vector[3:][len(self.uniqueLemmas):][len(self.uniquePostags):][:len(self.uniqueBilemmas)]):
			for j in range(value):
				bilemmas.append(self.uniquePostags[index])					
		"""5th part: bipostags"""
		for index, value in enumerate(vector[3:][len(self.uniqueLemmas):][len(self.uniquePostags):][len(self.uniqueBilemmas):][:len(self.uniqueBipostags)]):
			for j in range(value):
				bipostags.append(self.uniquePostags[index])			
		return markers + lemmas + postags + bilemmas + bipostags
		
	def getKFoldModel(self, k=5):
		pass
	
	def save(self, path="model"):
		dumpFile = open(path, 'wb')
		mc = ModelContainer()
		mc.documents = self.documents
		mc.lemmasCount = self.lemmasCount
		mc.postagsCount = self.postagsCount
		mc.unknownCount = self.unknownCount
		mc.bilemmasCount = self.bilemmasCount
		mc.bipostagsCount = self.bipostagsCount
		mc.uniqueLemmas = self.uniqueLemmas
		mc.uniquePostags = self.uniquePostags
		mc.uniqueBilemmas = self.uniqueBilemmas
		mc.uniqueBipostags = self.uniqueBipostags
		mc.isEmended = self.isEmended
		mc.isBigrams = self.isBigrams
		
		pickle.dump(mc, dumpFile)
		dumpFile.close()		
					
	def mergeModels(self,addedModel):
		self.documments += addedModel.documments
		
	def trimModel(self, n=5):
		pass	

	def load(self,path):
		dumpFile = open(path,'r')  
		mc =  pickle.load(dumpFile) 
		self.documents = mc.documents
		self.lemmasCount = mc.lemmasCount
		self.postagsCount = mc.postagsCount
		self.unknownCount = mc.unknownCount
		self.bilemmasCount = mc.bilemmasCount
		self.bipostagsCount = mc.bipostagsCount
		self.uniqueLemmas = mc.uniqueLemmas
		self.uniquePostags = mc.uniquePostags
		self.uniqueBilemmas = mc.uniqueBilemmas
		self.uniqueBipostags = mc.uniqueBipostags
		self.isEmended = mc.isEmended
		self.isBigrams = mc.isBigrams
							
class ModelContainer:
	def __init__(self):
		self.documents = []
		self.lemmasCount = dict()
		self.postagsCount = dict()
		self.unknownCount = dict()
		self.bilemmasCount = dict()
		self.bipostagsCount = dict()
		self.uniqueLemmas = []
		self.uniquePostags = []
		self.uniqueBilemmas = []
		self.uniqueBipostags = []
		self.isEmended = False
		self.isBigrams = False
		
