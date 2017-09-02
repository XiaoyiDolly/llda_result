#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    extract from llda_results_sweetwords & insert into mongo
'''
from pymongo import MongoClient
from insert_topics import readTopics, importTopics
client = MongoClient('localhost', 27019)
DB = client.nasa_publication

def runner():
    print "Insert topics..."
    topics = readTopics()
    importTopics(topics=topics, collection=DB.LLDA_topics_sweetwords)
    print "Done..."

if __name__ == "__main__":
    runner()
