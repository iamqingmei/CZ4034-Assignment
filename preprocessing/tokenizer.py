import nltk.data
import json
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import os

TOPICS = ['entertainment','health','local','money','opinions','politics','sport','style','travel']

PATH = './data/'
STOP = stopwords.words('english') + list(string.punctuation) + [',"', '."', '--']
CONTENTS = ['title', 'description', 'text']
LEMMATIZER = WordNetLemmatizer()

def word_tokenize(text):
    word_list = [LEMMATIZER.lemmatize(i) for i in wordpunct_tokenize(text.lower()) if i not in STOP]
    return word_list

def main():

    id = 1

    for topic in TOPICS:
        path = PATH + topic
        directory = os.fsencode(path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".json"):
                data = json.load(open(path + '/' + filename))
                data.pop('localpath', None)
                data.pop('date_download', None)
                data.pop('date_modify', None)
                data.pop('filename', None)
                data["id"] = id
                id += 1
                for content in CONTENTS:
                    if content in data.keys() and data[content] != None:
                        new_content = word_tokenize(data[content])
                        data[content] = new_content
                with open(path + '/' + filename, 'w') as outfile:
                    json.dump(data, outfile)

main()
