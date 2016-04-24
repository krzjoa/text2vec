# coding=utf-8
import aspell

class Correct:
    def __init__(self):
        self.s = aspell.Speller(('lang','pl'),('master', '/home/krzysztof/Pulpit/Projekt/pl/pl.rws'))
        
    def correct(self,word):
        suggested = self.s.suggest(word)
        print "Suggested", suggested
        if len(suggested)>0:
            return suggested[0]
        else:
            return '_UNK_'
        
    def suggest(self, word):
        return self.s.suggest(word)
