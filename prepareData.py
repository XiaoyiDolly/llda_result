#!/usr/bin/python
# -*- coding: utf-8 -*-
from pymongo import MongoClient
import pprint
from lxml import etree
from bs4 import BeautifulSoup
import re, csv, os

client = MongoClient('hawking.sv.cmu.edu', 27019)
DB = client.nasa_publication
dst_collection = DB.LLDA_input

pre_re_arr = [re.compile(r' *?\[.*?<a.*?>.*?<\/a>.*?\]'),
	re.compile(r' *?<em>.*?et al\..*?<\/em>')]


post_re_arr = [re.compile(r'[()]'),
	re.compile(r' +')]

'''
	Format of k1\k2: word1 word2; word3 word4 word5; word6 word7（There keyword in total）
	Regenerate:
		all words to lower case
		Use '/' as interval of word in one key. Use ' ' as interval of different keys

'''
def gen_keywords(k1, k2):
	k1 = k1.lower()
	k2 = k2.lower()

	k_set = set([k.strip() for k in k1.split(";")] + [k.strip() for k in k2.split(";")])
	return " ".join([k.replace(" +", " ").replace(" ", "/") for k in k_set]).strip()


def clean_mainbody(text):
	# text = re.sub(r' *?\[[0-9]+\]', "", text)
	# text = re.sub(, "", text)
	# text = re.sub(r' *?\[.*?<a.*?>.*?<\/a>.*?<em>.*?<\/em>.*?\]', "", text)
	# text = re.sub(r' *?<em>.*?et al\..*?<\/em>', "", text)
	for r in pre_re_arr:
		text = r.sub("", text)
	# print "text:" + text
	soup = BeautifulSoup(text)
	clean_str = ""
	# Only remains paragraphs
	for node in soup.findAll('p'):
		clean_str += ' '.join(node.findAll(text=True))

	for r in post_re_arr:
		clean_str = r.sub(" ", clean_str)

	return clean_str


def insertDataIntoMongo(document_id, keywords, text):
	print document_id
	print keywords
	dst_collection.insert_one({
			'document_id': document_id,
			"keywords": keywords,
			"text": text
		})


def getAllMetadatas():
	metadatas = {}
	metadata_list = list(client.paper_content.paper_metadata.find(
					{"document_id":{"$exists" : True}},
					{"document_id" : 1, 'Title': 1, "Abstract": 1, "Authour Keyword": 1, "Keywords2" : 1}))
	for m in metadata_list:
		metadatas[m['document_id']] = m
	return metadatas

'''
	 Title, Abstract, mainbody (w/o acknoledgement), remove “… et al.”/citations/”()”
'''
def concactTextAndInsert(metadatas):
	dst_collection.drop()
	for doc in client.nasa_publication.mainbody.find({"mainbody_backup":{"$exists" : True}}, {'document_id': 1, 'mainbody_backup':1}):
		document_id = doc['document_id']

		print "Process:" + str(document_id)
		mainbody_backup = doc['mainbody_backup']
		mainbody = clean_mainbody(mainbody_backup)
		# print mainbody
		keywords = get_keywords_by_id(metadatas, document_id)
		if keywords is None or len(keywords) == 0:
			continue
		text = " ".join([i for i in [metadata['Title'], metadata['Abstract'], mainbody] if i is not None])
		insertDataIntoMongo(document_id, keywords, text)

'''
	document_id: str
'''
def get_keywords_by_id(metadatas, document_id):
	metadata = metadatas[document_id]
	# print metadata
	if metadata['Title'] is not None:
		metadata['Title'] += "."
	if metadata['Abstract'] is not None:
		for r in post_re_arr:
			metadata['Abstract'] = r.sub(" ", metadata['Abstract'])

	return gen_keywords(metadata['Authour Keyword'], metadata['Keywords2'])

def gen_csv(src_coll=dst_collection):
	APP_ROOT = os.path.dirname(os.path.abspath(__file__))

	FILE_PATH = os.path.join(APP_ROOT, 'data')
	input_file_name = "TopicTermtop5.csv"
	input_file = os.path.join(FILE_PATH, input_file_name)
	writer = csv.writer(open(input_file, "w"), delimiter=',')
	for doc in dst_collection.find():
		writer.writerow([doc['document_id'], doc['keywords'], doc['text_sweet_words'].encode('utf-8')])



def runner():
	metadatas = getAllMetadatas()
	concactTextAndInsert(metadatas)
	os.system('./filter_non_sweet_words.py')
	gen_csv()
	print "Done."

if __name__ == "__main__":
	runner()