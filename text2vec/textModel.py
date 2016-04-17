# coding=utf-8
from operator import add
from collections import Counter
import string
import tools as t
import cPickle as pickle
import textTransformer as tt

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
	
	def compute(self):
		self.lemmas, self.unknownLemmas = t.lemmatize(self.tokenized)	
		self.postags , self.unknownPostags = t.pos(self.lemmas)
		
	def countBillemas(self):
		pass
	
	def countBipostags(self):
		pass		
		
class TextModel:
	def __init__(self):
		self.documents = []
		self.lemmatizer = tt.TextTransformer()
		self.lemmasCount = dict()
		self.postagsCount = dict()
		self.unknownCount = dict()
		self.uniqueLemmas = []
		self.uniquePostags = []
		self.lemmaNgrams = 0
		self.postagsNgrams = 0
			
	def fit(self,documents, labels, autocorrect=False):
		self.documents  = [Document(i, j) for i, j in  zip(documents, labels)]
		pos, unk, lem, mark  = self.lemmatizer.transform(documents)
		for p, u, l, m, document in zip(pos, unk, lem, mark, self.documents):
			document.lemmas = l
			document.postags = p
			document.unknown = u
			document.markers = m
		if autocorrect: self.emend()
		self._computeVectorModel()					

	def _computeVectorModel(self):			
		self.lemmasCount = dict(Counter(reduce(add,[document.lemmas for document in self.documents])))
		self.postagsCount = dict(Counter(reduce(add,[document.postags for document in self.documents])))
		self.unknownCount = dict(Counter(reduce(add,[document.unknown for document in self.documents])))
		self.uniqueLemmas = list(self.lemmasCount)
		self.uniquePostags = list(self.postagsCount)
		
	def emend(self):
		print "Start"
		newPos, newUnk, newLem, emendationLogs = self.lemmatizer.autocorrect(self.documents)
		for l, p, u, eml, document in zip(newLem, newPos, newUnk, emendationLogs, self.documents):
			document.lemmas = l
			document.postags = p
			document.unknown = u
			document.emendationLogs=eml	
		self._computeVectorModel()	
		
	# Get lemmas, postags, unknown, markers
		
	def getLemmas(self):
		return [document.lemmas for document in self.documents]	
		
	def getUniqueLemmas(self):
		return self.uniqueLemmas
	
	def getLemmasFreq(self):
		return sorted(self.lemmasCount.items(), key=lambda x:x[1], reverse=True)		
		
	def getPostags(self):
		return [document.postags for document in self.documents]	
		
	def getUniquePostags(self):
		return self.uniquePostags
		
	def getPostagsFreq(self):
		return sorted(self.postagsCount.items(), key=lambda x:x[1], reverse=True)			
		
	def getUnknown(self):
		return [document.unknown for document in self.documents]
	
	def getUniqueUnknown(self):
		return set(reduce(add,self.getUnknown))	
		
	def getUnknownFreq(self):
		return sorted(self.unknownCount.items(), key=lambda x:x[1], reverse=True)		
		
	def getEmendationLogs(self):
		return [document.emendationLogs for document in self.documents]
	
	def getAllEmendationLogs(self):
		return reduce(add,self.getEmendationLogs())			
		
	def getVectors(self):
		lemmasVecs =  [[document.lemmas.count(word) for word in self.uniqueLemmas] for document in self.documents]
		postagsVecs = [[document.postags.count(posTag) for posTag in self.uniquePostags] for document in self.documents]
		marksVecs = [document.marks for document in self.documents]
		x = [l+p+m for l, p, m in zip(lemmasVecs, postagsVecs, marksVecs)]
		y = [document.label for document in self.documents]
		return x, y
		
	def vectorize(self, text):
		document = Document(text)
		pos, unk, lem, mark = self.lemmatizer.transform([text])
		document.postags, document.unknown, document.lemmas, document.markers = pos[0], unk[0], lem[0], mark[0]
		lemmasVec =  [document.lemmas.count(word) for word in self.uniqueLemmas]	
		postagsVec =  [document.postags.count(posTag) for posTag in self.uniquePostags]	
		return lemmasVec + postagsVec + document.markers
			
	def devectorize(self, vector):
		words = []
		postags = []
		markers = []
		"""1st part of vector = lemmas """
		for index, value in enumerate(vector[:len(self.uniqueLemmas)]):
			for j in range(value):
				words.append(self.uniqueLemmas[index])
		"""2nd part of vector = postags """		
		for index, value in enumerate(vector[len(self.uniqueLemmas):][:-3]):
			for j in range(value):
				postags.append(self.uniquePostags[index])		
		"""3rd part of vector = markers"""
		markers = vector[-3:]		
		return words + postags + markers
		
	def getKFoldModel(self, k=5):
		pass
	
	def save(self, path="model"):
		dumpFile = open(path, 'wb')
		modelConainer = ModelContainer(self.documents, self.lemmasCount, self.postagsCount, self.uniqueLemmas, self.uniquePostags)
		pickle.dump(modelConainer, dumpFile)
		dumpFile.close()		
					
	def mergeModels(self,addedModel):
		self.documments += addedModel.documments
		
	def trimModel(self, n=5):
		pass	

	def load(self,path):
		dumpFile = open(path,'r')  
		modelConainer =  pickle.load(dumpFile) 
		self.documents = modelConainer.documents
		self.lemmasCount = modelConainer.lemmasCount
		self.postagsCount = modelConainer.postagsCount
		self.uniqueLemmas = modelConainer.uniqueLemmas
		self.uniquePostags = modelConainer.uniquePostags
							
class ModelContainer:
	def __init__(self, d, lc, pc, ul, up):
		self.documents = d
		self.lemmasCount = lc
		self.postagsCount = pc
		self.uniqueLemmas = ul
		self.uniquePostags = up
