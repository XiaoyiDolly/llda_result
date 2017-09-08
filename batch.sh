#!/bin/bash
if [ $# -ne 2 ]; then
	echo $0 "id_lower_bound(inclusive) id_upper_bound(exclusive)"
else
	rm -f data/TopicTermtop5.csv.term-counts.cache.*.gz
	./prepareData.py $1 $2 && ./run.py TopicTermtop5.csv && ./insert_topics.py && ./summary_LLDA_topics.py data/summary.txt 
fi
