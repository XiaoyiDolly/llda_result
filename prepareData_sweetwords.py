#!/usr/bin/python
# -*- coding: utf-8 -*-
from prepareData import getAllMetadatas, gen_csv, get_keywords_by_id
from pymongo import MongoClient
import sys

client = MongoClient('hawking.sv.cmu.edu', 27019)
DB = client.nasa_publication
dst_collection = DB.LLDA_input_sweetwords

'''
	Use sweet words inside the publication as the input
'''
def concactSweetWordsAndInsert(metadatas, noSplit=False):
	dst_collection.drop()
	for doc in DB.paper_sweet_words.find({}, {'document_id': 1, 'sweet_words':1}):
		# concat all sweet_words by its frequency
		text_sweet_words = ""
		word_map = doc['sweet_words']
		for root in word_map:
			for word_item in word_map[root]:
				# Option 1: 'dust dorm' * 2 -> "dust dorm dust dorm"
				if not noSplit:
					text_sweet_words += " ".join([word_item['word']] * word_item['count']) 
				# Option 2 : 'dust dorm' * 2 -> "dustdorm dustdorm"
				if noSplit:
					text_sweet_words += " ".join([word_item['word'].replace(" ", "")] * word_item['count'])  
				text_sweet_words += " "
		text_sweet_words = text_sweet_words.strip()
		document_id = doc['document_id']
		keywords = get_keywords_by_id(metadatas, document_id)
		if keywords is None or len(keywords) == 0:
			continue
		dst_collection.insert_one({
					'document_id': document_id,
					"keywords": keywords,
					"text_sweet_words": text_sweet_words
				})

def runner():
	global 	dst_collection
	print "Prepareing Data..."
	metadatas = getAllMetadatas()
	if len(sys.argv) == 4 and sys.argv[3] == "noSplit": # noSplit
		dst_collection = DB.LLDA_input_sweetwords.noSplit
		concactSweetWordsAndInsert(metadatas, noSplit=True)
		gen_csv(src_coll=dst_collection, input_text_column="text_sweet_words", lower_bound=int(sys.argv[1]), upper_bound=int(sys.argv[2]))
	elif len(sys.argv) == 3:
		concactSweetWordsAndInsert(metadatas)
		gen_csv(src_coll=dst_collection, input_text_column="text_sweet_words", lower_bound=int(sys.argv[1]), upper_bound=int(sys.argv[2]))
	else:
		gen_csv(src_coll=dst_collection, input_text_column="text_sweet_words")	
	print "Done."

if __name__ == "__main__":
	runner()