#!/usr/bin/python
# -*- coding: utf-8 -*-
print 'Initializing imports...'

import pickle

import numpy as np
import lda

from nltk.tokenize import RegexpTokenizer

from nltk.stem.porter import PorterStemmer

p_stemmer = PorterStemmer()

from stop_words import get_stop_words

en_stop = get_stop_words('en')

from gensim import corpora, models
from gensim.models.ldamodel import LdaModel
import gensim

import json
import os.path

from pymongo import MongoClient

client = MongoClient(host="hawking.sv.cmu.edu", port=27019)


sciWords = set()

for i in client.paper_content.sci_words.find():
	for j in i['word'].replace("'s", '').split(' '):
		if len(j) >= 3:
			sciWords.add(p_stemmer.stem(j.lower()))

for i in en_stop:
	i = p_stemmer.stem(i)
	if i in sciWords:
		sciWords.remove(i)

print sciWords
	

import os

tokenizer = RegexpTokenizer(r'\w+')

def getBow(text):
	raw = text.lower()
	tokens = tokenizer.tokenize(raw)
	tokens = [p_stemmer.stem(i) for i in tokens if p_stemmer.stem(i) in sciWords]
	return ' '.join(tokens)

print "updating"

coll = client.nasa_publication.LLDA_input
for i in coll.find():
 	text = i['text']
 	processed = getBow(text)
 	i['text_processed'] = processed
 	_id = i['_id']
 	del i['_id']
 	coll.update({"_id": _id}, i)



