from pymongo import MongoClient

client = MongoClient('localhost', 27019)
db = client.nasa_publication
topic_fn = "document-topic-distributions.csv"
labels = "label-index.txt"
topics=[]

def readTopics():
    global topics
    with open(labels, "r") as labelFile:
        lines = labelFile.readlines()
        for l in lines:
            topics.append(l.strip())

def importTopics():
    collection = db.LLDA_topics
    collection.drop()
    with open(topic_fn, "r") as f1: # , open(attribute_matrix,"w") as f2:
        lines = f1.readlines()
        for l in lines:
            str = l.strip().split(",")
            id = int(str[0])
            i = 0
            topic_json = {
                "paper_id": id
            }
            topic_list=[]
            for s in str:
                if(i > 0 and i%2 == 0):
                    if float(s)<0: continue
                    if float(s)>1: s = 1
                    topic_percent = {
                        "topic":topics[int(str[i-1])].replace("/"," "),
                        "percent":float(s)
                    }
                    # print(topic_percent)
                    topic_list.append(topic_percent)
                i+=1
            if len(topic_list) ==0: continue
            topic_json["topics"] = topic_list
            print(topic_json)

            collection.update_one({
                'paper_id': id
            }, {'$set': {
                    # 'plain_text': html_str,
                    'topics': topic_list
                }}, True)


readTopics()
importTopics()