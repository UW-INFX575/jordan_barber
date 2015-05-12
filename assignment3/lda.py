import numpy as np
import lda
import lda.datasets
import csv
from gensim import corpora, models, similarities
import gensim
import urllib.request
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from collections import Counter
from nltk import bigrams
from nltk import trigrams
from nltk.collocations import *
import nltk
import csv
import re

# create stopper for english words
go_stop = get_stop_words('en')

# create Porter stemmer
go_stem = PorterStemmer()

# create tokenizer using regex \w+ method
tokenizer = RegexpTokenizer(r'\w+')

dir = "insert a directory"
page_id = ["insert list of page IDs"]

# initilize lists for loop
all_uni_grams = []
all_bi_grams = []
all_tri_grams = []

texts = []

for i in page_id:
    # construct url
    url = dir + i + ".txt"
    
    # dump source into page
    page = urllib.request.urlopen(url)
    
    # convert url to readable raw, lower-case string
    raw = page.read()
    raw = raw.decode('utf-8')
    raw = raw.lower()

    # tokenize raw
    tokens = tokenizer.tokenize(raw)

    # remove stop words from tokens
    stopped = [i for i in tokens if not i in go_stop]

    # stem tokens
    stemmed = [go_stem.stem(i) for i in stopped]
    
    texts.append(stemmed)  

dictionary = corpora.Dictionary(texts)

corpus = [dictionary.doc2bow(text) for text in texts]

ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=5, id2word = dictionary, passes=20)

print(ldamodel.print_topics(5, 5))
