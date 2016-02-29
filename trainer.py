#!/usr/bin/python2.7
import gensim
import cython
import sys
import pdb

#class MySentences(object):
    #def __init__(self, filename):
        #self.filename = filename
        #self.file = open(filename,'r')

    #def __iter__(self):
     #   yield self.file.readline().strip().split(' ')

filename = '/opt/projects/domain_nlp/sentences.nocaps'
sentences = [sentence.strip().split(' ') for sentence in open(filename).readlines()]
model = gensim.models.Word2Vec(workers=24, size=800)
print "Building vocab.."
model.build_vocab(sentences)
print "Vocab done. Training."
model.train(sentences)
print "Training done. Saving to /opt/projects/domain_nlp/hn_model"
model.save('/opt/projects/domain_nlp/hn_model')
print "Training done. pdbing."


#model.train(sentences, workers=24, size=400, min_count=10)
