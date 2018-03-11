
# coding: utf-8

# In[ ]:

from sklearn.externals import joblib
import string
from nltk.stem.porter import *
import nltk 
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
lemmer = WordNetLemmatizer()
import numpy as np


# In[ ]:


count_vector = joblib.load('../Model/count_vector.pkl') 
naive_bayes = joblib.load('../Model/naive_bayes.pkl') 
d = {0: 'local', 1: 'politics', 2: 'sport', 3: 'health', 4: 'money'}


# In[ ]:


# title = ["Navarro says 'no exclusions' on steel and aluminum tariffs"]
# text = ["Washington (CNN) White House trade adviser Peter Navarro says no countries will be excluded from upcoming steel and aluminum tariffs set to be imposed by the Trump administration, including the United States' greatest allies.\n\"There's a difference between exemptions and country exclusions,\" Navarro, the director of the White House Office of Trade and Manufacturing Policy, said Sunday on CNN's \"State of the Union.\" \"There will be an exemption procedure for particular cases where we need to have exemptions so that business can move forward, but at this point in time, there will be no country exclusions.\"\nNavarro said he expects President Donald Trump to sign the measures by the end of this week or early in the next.\nThe President has long cited Chinese overproduction of steel as a reason to impose tariffs. However, US allies such as Canada and South Korea account for a larger share of American steel imports than China.\n\"The bigger picture here is that China has tremendous overcapacity in both aluminum and steel, and so what they do is flood the world market with this product, and this ripples down to our shores and to other countries,\" Navarro said when asked about the issue. \"And so China is in many ways the root of the problem for both aluminum and steel for all countries of the world.\""]


# In[ ]:

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
    title_lower = [x.lower().translate(str.maketrans('','', string.punctuation)) for x in title]
    text_lower = [x.lower().translate(str.maketrans('','', string.punctuation)) for x in text]
    title_lem = [' '.join([lemmer.lemmatize(w) for w in nltk.word_tokenize(x) if w not in stopwords.words('english')]) for x in title_lower]
    text_lem = [' '.join([lemmer.lemmatize(w) for w in nltk.word_tokenize(x) if w not in stopwords.words('english')]) for x in text_lower]
    title_text_lem = []
    for i in range(len(title_lem)):
        title_text_lem.append(title_lem[i] + text_lem[i])
    title_text_lem = np.array(title_text_lem)
    
    x = count_vector.transform(title_text_lem)
    prediction_result = naive_bayes.predict(x)
    return [d[i] for i in prediction_result]
    

