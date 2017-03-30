#!/usr/bin/python
# -*- coding: utf-8 -*-
from pymongo import MongoClient

import re, sys, csv


client = MongoClient('hawking.sv.cmu.edu', 27019)


years = [1969,1970,1971,1972,1973,1974,1975,1977,1978,1979,1980,1981,1982,1983,1984,1985,1986,1987,1988,1989,1990,1991,1992,1993,1994,1996,1999,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016]

def getTopicMap():
	topicMap = {}
	for doc in client.nasa_publication.topic_overview.find():
		topic = {}
		topic_name = doc['topic']
		topic['topic'] = topic_name
		topic['year_count'] = {}
		for y in years:
			topic['year_count'][str(y)] = 0
		topicMap[topic_name] = topic

	return topicMap

'''
	traverse all publications
'''
def getTopicTrend():
	topicMap = getTopicMap()
	for doc in client.nasa_publication.LLDA_topics.find():
		metadata = client.paper_content.paper_metadata.find_one({'document_id':doc['paper_id']})
		year = metadata['Publication_Date'].strip()[-4:]
		for topic in doc['topics']:
			topic_name = topic['topic']
			
			# print topic_name
			topicMap[topic_name]['year_count'][year] += 1

	return topicMap


def formatTopicName(topic_name):
	return topic_name.upper().replace(" ", "_")

def generateTopicsCSV(topicMap, file_name):
	heading = ["CountryCode","RegionCode","RegionName"]
	writer = csv.writer(open(file_name, 'w'), delimiter=',')
	writer.writerow(heading)
	for key in topicMap:
		formated_topic_name = formatTopicName(key)
		writer.writerow([formated_topic_name,formated_topic_name,formated_topic_name])
	

def generateTrendCSV(topicMap, file_name):
	heading = ["CountryName","CountryCode"] + [str(i) for i in years]
	writer = csv.writer(open(file_name, 'w'), delimiter=',')
	writer.writerow(heading)
	for key in topicMap:
		writer.writerow([formatTopicName(key), formatTopicName(key)] + [topicMap[key]['year_count'][str(year)] for year in years])





def accTopicTrend(topicMap):
	for key in topicMap:
		for i in range(1, len(years)):
			topicMap[key]["year_count"][str(years[i])] += topicMap[key]["year_count"][str(years[i-1])]
	return topicMap 		

def helper():
	print('''
%s topics.csv topicTrend.csv topicTrend_acc.csv
		''' % (sys.argv[0]))

if __name__ == '__main__':
	if len(sys.argv) != 4:
		helper()
		sys.exit(1)
	topicMap = getTopicTrend()
	generateTopicsCSV(topicMap, sys.argv[1])
	generateTrendCSV(topicMap, sys.argv[2]) 
	topicMap_acc = accTopicTrend(topicMap)	
	generateTrendCSV(topicMap_acc, sys.argv[3])







