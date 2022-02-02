import pandas as pd
import numpy as np
import nltk
import matplotlib.pyplot as plt
import re
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

from nltk.corpus import wordnet
import string
from nltk.stem import WordNetLemmatizer, PorterStemmer


nltk.download('words')

from nltk.corpus import stopwords
nltk.download('stopwords')

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import spacy
nlp = spacy.load('en_core_web_sm')




from sklearn import metrics

from xgboost import XGBClassifier
import pickle

import matplotlib.pyplot as plt


import glob
import os
import pandas as pd
import re
import unicodedata
import spacy
import gensim

text = "#India has the largest number of ppl dying in road accidents. That + 99 more things to debate before we vote http://t.co/zkxbONv850"

stop_words=set( stopwords.words('english') )

ip_addr_regex = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
def regex_cleaning(phrase):
      # specific
  phrase = re.sub(r"won\'t", "will not", phrase)
  phrase = re.sub(r"can\'t", "can not", phrase)

  # general
  phrase = re.sub(r"n\'t", " not", phrase)
  phrase = re.sub(r"\'re", " are", phrase)
  phrase = re.sub(r"\'s", " is", phrase)
  phrase = re.sub(r"\'d", " would", phrase)
  phrase = re.sub(r"\'ll", " will", phrase)
  phrase = re.sub(r"\'t", " not", phrase)
  phrase = re.sub(r"\'ve", " have", phrase)
  phrase = re.sub(r"\'m", " am", phrase)
  phrase = re.sub(r"[^a-zA-Z0-9]+", " ", phrase)
  phrase = re.sub('[\(\[].*?[\)\]]', ' ', phrase)
  phrase = unicodedata.normalize('NFKD', phrase).encode('ascii', 'ignore').decode('utf-8', 'ignore')
  phrase = re.sub(r"\r\n", "", phrase)            # Removing additional line
  phrase = re.sub(r"\n", "", phrase)              # Removing additional line 
  phrase = re.sub(r"\S*@\S*\s?", "", phrase)      # Removing email-addresses 
  phrase = re.sub(r'http\S+', '', phrase)         # Removing website links
  phrase = re.sub(ip_addr_regex, "", phrase)      # Removing IP address link.
  phrase = emoji_pattern.sub(r'', phrase)         # Removing Emojis
  
  phrase_final = " ".join([word for word in phrase.split() if word not in stop_words and len(word) > 3])
  return phrase_final 


def gen_words(text):
  final = []
  # for text in texts:
  new = gensim.utils.simple_preprocess(text, deacc=True)
  for word in new:
    if len(word) > 3:
      final.append(word)
  # print(final)
  return (" ".join(final))

def lemmatization(texts, allowed_postags=["NOUN", "ADJ", "VERB", "ADV"]):
  nlp = spacy.load("en_core_web_sm")


  doc = nlp(texts)
  new_text = []
  for token in doc:
    if token.pos_ in allowed_postags:
      new_text.append(token.lemma_)
  
  return [" ".join(new_text)]
def final_prep_prop(text):
    
    file = open("tfidf_object.pkl",'rb')
    tf_idf = pickle.load(file)
    file = open("xgb_reg.pkl",'rb')
    model = pickle.load(file)

    reg_cl = regex_cleaning(text)
    final_text = lemmatization(reg_cl)
    tf_idf.transform(final_text)
    pred = model.predict(vec_text)
    return pred

reg_cl = regex_cleaning(text)
final_text = lemmatization(reg_cl)

file = open("tfidf_object.pkl",'rb')
tf_idf = pickle.load(file)

file = open("xgb_reg.pkl",'rb')
model = pickle.load(file)

vec_text = tf_idf.transform(final_text)

pred = model.predict(vec_text)

print(pred)