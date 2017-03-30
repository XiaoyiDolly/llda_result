#!/usr/bin/python
# -*- coding: utf-8 -*-
from pymongo import MongoClient

import re, sys




def helper():
	print('''
%s summary.txt
		''' % (sys.argv[0]))


def summary(input_summay_file):
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
						topic_map[topic_name] = {'topic': topic_name, 'keywords': list(topic_keywords), 'publication_counts': 0}
					topic_name = line.split("\t")[0].replace('/', ' ')
					topic_keywords = []
	if topic_name is not None:
		print topic_name
		topic_map[topic_name] = {'topic': topic_name, 'keywords': list(topic_keywords), 'publication_counts': 0}


	# print topic_map

	client = MongoClient('hawking.sv.cmu.edu', 27019)
	for doc in client.nasa_publication.LLDA_topics.find():
		for topic in doc['topics']:
			topic_name = topic['topic']

			# print topic_name
			topic_map[topic_name]['publication_counts'] += 1

	print topic_map

	client.nasa_publication.topic_overview.drop()
	for name in topic_map:
		# print topic_map[name]
		client.nasa_publication.topic_overview.update(topic_map[name],
			{
	  			'$set': {
	    			'topic': name
	  			}
			}, upsert=True)


def runner():
	if len(sys.argv) != 2:
		helper()
		exit(1)

	summary(sys.argv[1])

if __name__ == "__main__":
	runner()





