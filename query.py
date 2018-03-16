import json
import string
import os
import pysolr
from sklearn.externals import joblib
import string
from nltk.stem.porter import *
import nltk
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords

lemmer = WordNetLemmatizer()
import numpy as np

count_vector = joblib.load('./Model/count_vector.pkl')
naive_bayes = joblib.load('./Model/naive_bayes.pkl')
d = {0: 'local', 1: 'politics', 2: 'sport', 3: 'health', 4: 'money'}
STOP = stopwords.words('english') + list(string.punctuation) + [',"', '."', '--']
LEMMATIZER = WordNetLemmatizer()

def prediction(title, text):
    """
    example input:
    title: [title1,title2,title3]
    text: [text1,text2,text3]
    return: [result1,result2,result3]
    """
    if len(title) != len(text):
        print("The number of titles and text must be same!")
        return []
    title_lem = [' '.join(title[0])]
    text_lem = [' '.join(text[0])]
    title_text_lem = []
    for i in range(len(title_lem)):
        title_text_lem.append(title_lem[i] + text_lem[i])
    title_text_lem = np.array(title_text_lem)
    x = count_vector.transform(title_text_lem)
    prediction_result = naive_bayes.predict(x)
    return [d[i] for i in prediction_result]


def word_tokenize(text):
    word_list = [LEMMATIZER.lemmatize(i) for i in wordpunct_tokenize(text.lower()) if i not in STOP]
    return word_list

def query(keywords, topic):
    solr = pysolr.Solr('http://localhost:8983/solr/4034')
    keywords = word_tokenize(keywords)
    query = 'text: '
    for word in keywords:
        query = query + '"' + word + '"'

    results = solr.search(q=query, rows=25)
    final = []
    for result in results:
        pred = prediction([result['title']], [result['text']])
        if(pred[0] in topic):
            result['topic'] = pred[0]
            final.append(result)
    return final

query('Nanyang technological', ['money'])

