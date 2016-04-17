# coding=utf-8

import re
import string

def searchDots(text): #Znajduje wyrazy zawierające co najmniej 2 kropki
    return True if re.search('\.{2,}',text)!=None else False

def searchEmot(text): #Szuka ciągów składających się z co najmniej dwóch el. ze zbioru {!,?}
    return True if re.search('[!,?]{2,}',text)!=None else False

def searchUppercase(text): #Sprawdza, czy dany ciąg słów jest napisany z użyciem więcej niż jednego uppercase'a
    return True if re.search('[A-Z]{2,}',text)!=None else False

def clean(splittedText):
    x = [''.join(c for c in s if c not in string.punctuation) for s in splittedText]
    return [s for s in x if s]

def countUpper(text):
	"""Counts number of uppercase substrings"""
	return len(re.findall('[A-Z]{2,}',text))    

def countDotted(text):
	""" Counts number of substrings like '..', '.....' (i. e. containining two or more dots) """
	return len(re.findall('\.{2,}',text))

def countEmot(text):
	"""Counts number of substrings containig ! or ? """
	return len(re.findall('[!,?]{2,}',text))

