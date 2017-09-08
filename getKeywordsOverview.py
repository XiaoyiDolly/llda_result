#!/usr/bin/python
# -*- coding: utf-8 -*-
from pymongo import MongoClient

client = MongoClient('hawking.sv.cmu.edu', 27019)
DB = client.nasa_publication
src_coll = DB.LLDA_input
dst_coll = DB.LLDA_keywordOverview

def run():
	print "start..."
	dst_coll.drop()
	id_keywords_list = list(src_coll.find(
					{"document_id":{"$exists" : True}},
					{"document_id" : 1, 'keywords': 1}))
	keywords = {}
	for item in id_keywords_list:
		for k in item['keywords'].split(" "):
			if k not in keywords:
				keywords[k] = set()
			keywords.get(k).add(item["document_id"])
	
	for k in keywords:
		dst_coll.insert_one({
				"keyword": k,
				"document_ids": list(keywords.get(k))
			})
	print "Done"



if __name__ == "__main__":
	run()

