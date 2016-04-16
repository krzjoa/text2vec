# coding=utf-8
from operator import add
from collections import Counter
import string
import tools
import cPickle as pickle

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
		self.lemmatizer = tools.LemmPosTagger()
		self.lemmasCount = dict()
		self.postagsCount = dict()
		self.uniqueLemmas = []
		self.uniquePostags = []
			
	def fit(documents, labels):
		self.documents = [Document(i, j) for i, j in  zip(documents, labels)]
		self.pos, self.unk, self.lem = self.lemmatizer.transform(documents)
		for x,y,z, document in zip(self.pos, self.unk, self.lem, self.documents):
			document.lemmas = z
			document.postags = x
			document.unknown = y					

	def unknown(self):
		all_unknown = set(reduce(add, [i.unknownLemmas for i in self.comments]))
		return all_unknown
		
	def setVectorModel(self):			
		self.lemmasCount = dict(Counter(reduce(add,[i.lemmas for i in self.comments])))
		self.postagsCount = dict(Counter(reduce(add,[i.postags for i in self.comments])))
		self.uniqueLemmas = list(self.lemmasCount)
		self.uniquePostags = list(self.postagsCount)
		
	def emendModel(self):
		newPos, newUnk, newLem = self.lemmatizer.emend(self.pos, self.unk, self.lem )
		for x,y,z, document in zip(newPos, newUnk, newLem , self.documents):
			document.lemmas = z
			document.postags = x
			document.unknown = y	
		
	#~ def countBillemas(self):
		#~ pass			
		
	def getAllLemmas():
		allLemmas = list()
		for i in self.documents:
			allLemmas.append(i.lemmas)
		return allLemmas		
		
	#~ def wordFreq(self, n=10):
		#~ table = PrettyTable(["Term", "Frequency"])
		#~ sortedTermsFreq = sorted(self.lemmasCount.items(), key=lambda x:x[1], reverse=True)
		#~ for i in sortedTermsFreq[:n]:
			#~ table.add_row([i[0],i[1]])
		#~ table.sort_key("Frequency")
		#~ return table	
	#~ 
	#~ def postagsFreq(self,n=10):
		#~ table = PrettyTable(["Term", "Frequency"])
		#~ sortedTermsFreq = sorted(self.postagsCount.items(), key=lambda x:x[1], reverse=True)
		#~ for i in sortedTermsFreq[:n]:
			#~ table.add_row([i[0],i[1]])
		#~ table.sort_key("Frequency")
		#~ return table	
		
	def getVectors(self):
		lemmasVecs =  [[documents.lemmas.count(word) for word in self.uniqueLemmas] for document in self.documents]
		postagsVecs = [[document.postags.count(posTag) for posTag in self.uniquePostags] for document in self.documents]
		x = [i+j for i,j in zip(lemmasVecs, postagsVecs)]
		y = [document.label for document in self.documents]
		return x, y
		
	def vectorize(self, text):
		document = Document(text)
		pos, unk, lem = self.lemmatizer.transform([text])
		document.postags, document.unknown, document.lemmas = pos[0], unk[0], lem[0]
		lemmasVec =  [document.lemmas.count(word) for word in self.uniqueLemmas]	
		postagsVec =  [document.postags.count(posTag) for posTag in self.uniquePostags]	
		return lemmasVec + postagsVec
			
	def devectorize(self, vector):
		words = []
		postags = []
		for index, value in enumerate(vector[:len(self.uniqueLemmas)]):
			for j in range(value):
				words.append(self.uniqueLemmas[index])
		for index, value in enumerate(vector[len(self.uniqueLemmas):]):
			for j in range(value):
				postags.append(self.uniquePostags[index])		
		return words + postags	
		
	def getKFoldModel(self, k=5):
		pass
	
	def save(self, path="model"):
		dumpFile = open(path, 'wb')
		modelConainer = ModelContainer(self.documents, self.lemmasCount, self.postagsCount, self.uniqueLemmas, self.uniquePostags)
		pickle.dump(modelConainer, dumpFile)
		dumpFile.close()		
					
	def mergeModels(self,addedModel):
		self.comments += addedModel.comments
		
	def trimModel(self, n=5):
		pass	

	def load(path):
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

		
						
