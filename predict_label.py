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
import warnings
warnings.filterwarnings('ignore')
from sklearn import metrics
import pickle
import matplotlib.pyplot as plt
import pandas as pd
import re
import unicodedata
import gensim

test_text = "#India has the largest number of ppl dying in road accidents. That + 99 more things to debate before we vote http://t.co/zkxbONv850"

"""Functions to clean text using Regex"""
ip_addr_regex = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

stop_words=stopwords.words('english') + ['&amp','&amp;']
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
    
    # phrase_final = " ".join([word.lower() for word in phrase.split() if word not in stop_words and len(word) > 3])
    phrase_final = [word.lower() for word in phrase.split() if word not in stop_words and len(word) > 3]
    return "" if len(phrase_final) < 3 else " ".join(phrase_final)  

# def word_2_vec_train(df_corpus):
#   story = []
#   clean_corpus = df_corpus.apply(regex_cleaning)
#   for doc in clean_corpus:
#       raw_sent = sent_tokenize(doc)
#       for sent in raw_sent:
#           story.append(simple_preprocess(sent))
#   model_gensim = gensim.models.Word2Vec( 
#       window=10,
#       min_count=2
#   )
#   model_gensim.build_vocab(story)
#   model_gensim.train(story, total_examples=model_gensim.corpus_count, epochs=model_gensim.epochs)

#   # remove out-of-vocabulary words
#   doc = [word for word in doc.split() if word in model_gensim.wv.index2word]
#   return model_gensim, np.mean(model_gensim.wv[doc], axis=0)

def word_2_vec_transform(doc, model_gensim):
  clean_doc = regex_cleaning(doc)
  final_doc = [word for word in clean_doc.split() if word in model_gensim.wv.index2word]
  return np.mean(model_gensim.wv[final_doc], axis=0)




def final_prep_prop(test_text, model_gensim):
      return model.predict(word_2_vec_transform(test_text, model_gensim).reshape(1, -1))[0]


file_gensim = open("model_gensim_label.pkl",'rb')
model_gensim = pickle.load(file_gensim)

file_model = open("model_label_generator_SVC_0.77.pkl",'rb')
model = pickle.load(file_model)


pred = final_prep_prop(test_text, model_gensim)

print(f"Given Text: {test_text} \nPredictied Label: {pred}")

