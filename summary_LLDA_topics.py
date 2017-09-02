#!/usr/bin/python
# -*- coding: utf-8 -*-
from pymongo import MongoClient

import re, sys

client = MongoClient('hawking.sv.cmu.edu', 27019)



def helper():
	print('''
%s summary.txt
		''' % (sys.argv[0]))


def summary(input_summay_file, dst_coll):
	topic_map = {}

	with open(input_summay_file, 'r') as f:
		topic_name = None
		topic_keywords = []
		for line in f.readlines():
			if line.strip() == '' or line.strip() == '\n':
				continue
			else:
				# print line
				if line.startswith('\t'):  # second hierarchical topic
					topic_keywords.append(line.strip().split("\t")[0])
					# print topic_keywords
				else: # first hierarchical topic 
					if topic_name is not None:
						print topic_name
						topic_map[topic_name] = {'topic': topic_name, 'keywords': list(topic_keywords), 'publication_counts': 0, 'publication_ids':[]}
					topic_name = line.split("\t")[0].replace('/', ' ')
					topic_keywords = []
	if topic_name is not None:
		print topic_name
		topic_map[topic_name] = {'topic': topic_name, 'keywords': list(topic_keywords), 'publication_counts': 0, 'publication_ids':[]}


	# print topic_map

	for doc in client.nasa_publication.LLDA_topics.find():
		paper_id = doc['paper_id']
		for topic in doc['topics']:
			topic_name = topic['topic']
			
			# print topic_name
			topic_map[topic_name]['publication_counts'] += 1
			topic_map[topic_name]['publication_ids'].append(paper_id)

	print topic_map

	dst_coll.drop()
	topic_id = 0
	for name in topic_map:
		# print topic_map[name]
		topic = topic_map[name]
		topic['topic_id'] = topic_id
		topic_id += 1
		dst_coll.insert_one(topic)


def runner(dst_coll=client.nasa_publication.topic_overview):
	if len(sys.argv) != 2:
		helper()
		exit(1)

	summary(sys.argv[1], dst_coll)

if __name__ == "__main__":
	runner()





