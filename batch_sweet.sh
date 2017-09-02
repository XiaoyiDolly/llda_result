#!/bin/bash


#
# Experiments for using sweets word + keywords as input instaed of text.
# Use different output table.
#
#

./prepareData_sweetwords.py && ./run.py && ./insert_topics_sweetwords.py && ./summary_LLDA_topics_sweetwords.py data/summary.txt && echo 'Everything done!'