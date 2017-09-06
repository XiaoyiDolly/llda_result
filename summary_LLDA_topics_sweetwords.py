#!/usr/bin/python
# -*- coding: utf-8 -*-
from pymongo import MongoClient
from summary_LLDA_topics import runner

client = MongoClient('hawking.sv.cmu.edu', 27019)

if __name__ == "__main__":
	runner(src_coll=client.nasa_publication.LLDA_topics_sweetwords, dst_coll=client.nasa_publication.topic_overview_sweetwords)


