#!/bin/bash


#
# Experiments for using sweets word + keywords as input instaed of text.
# Use different output table.
#
#
if [ $# -ne 2 ]; then
	echo $0 "id_lower_bound(inclusive) id_upper_bound(exclusive)"
else
	rm -f data/TopicTermtop5.csv.term-counts.cache.*.gz
	./prepareData_sweetwords.py $1 $2 noSplit && ./run.py TopicTermtop5.csv && ./insert_topics_sweetwords.py noSplit && ./summary_LLDA_topics_sweetwords.py data/summary.txt noSplit && echo 'Everything done!' 
fi