#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
    insert sweets words of all papers
'''

from pymongo import MongoClient
import requests
client = MongoClient(host="hawking.sv.cmu.edu", port=27019)


def getBow(text):
        r = requests.post('http://hawking.sv.cmu.edu:9054/sweetWords/getSweetWords', json={'text':text})
        sweet_words = r.json()
        res = ""
        for w in sweet_words:
                word = ' '.join(w['word'])
                for i in range(0, w['count']):
                        res += ' ' + word
        return res.strip() 
              


print "updating"

coll = client.nasa_publication.LLDA_input
text_list = list(coll.find())
for i in text_list:
	print "update " + str(i['document_id'])
        text = i['text']
        processed = getBow(text)
        i['text_sweet_words'] = processed
        _id = i['_id']
        del i['_id']
        coll.update({"_id": _id}, i)
