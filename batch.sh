#!/bin/bash

./prepareData.py && ./run.py && ./insert_topics.py && ./summary_LLDA_topics.py data/summary.txt && sudo ./gen_LLDA_topic_trend_csv.py /home/yankai/dustKnowledgeGraph/dustKnowledgeGraph/DustSocialNetwork-Frontend/public/data/topics.csv /home/yankai/dustKnowledgeGraph/dustKnowledgeGraph/DustSocialNetwork-Frontend/public/data/topicTrend.csv /home/yankai/dustKnowledgeGraph/dustKnowledgeGraph/DustSocialNetwork-Frontend/public/data/topicTrend_acc.csv && echo "Everthing Done!"

