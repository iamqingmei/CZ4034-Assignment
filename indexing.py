import json
import string
import os
import pysolr

TOPICS = ['entertainment','health','local','money','opinions','politics','sport','style','travel']

PATH = './tokenized_data/'


def main():
    solr = pysolr.Solr('http://localhost:8983/solr/4034')
    for topic in TOPICS:
        path = PATH + topic
        directory = os.fsencode(path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".json"):
                data = json.load(open(path + '/' + filename))
                list.append(data)
    solr.add(list)

main()
