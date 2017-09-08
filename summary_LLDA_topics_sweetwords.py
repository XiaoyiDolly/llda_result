#!/usr/bin/python
# -*- coding: utf-8 -*-
from pymongo import MongoClient
from summary_LLDA_topics import runner
import sys
client = MongoClient('hawking.sv.cmu.edu', 27019)

if __name__ == "__main__":
	if len(sys.argv) == 3 and sys.argv[2] == "noSplit": # noSplit
		runner(src_coll=client.nasa_publication.LLDA_topics_sweetwords_noSplit, dst_coll=client.nasa_publication.topic_overview_sweetwords_noSplit)
	else:
		runner(src_coll=client.nasa_publication.LLDA_topics_sweetwords, dst_coll=client.nasa_publication.topic_overview_sweetwords)


