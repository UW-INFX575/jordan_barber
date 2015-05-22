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
import scipy.stats
from statistics import mean
import re
import math
import numpy as np
import time
from scipy import cluster
import matplotlib.pylab as plt

# create stop list
go_stop = ["all","just","being","over","both","through","yourselves","its","before","herself","had","should","to","only","under","ours","has","do","them","his","very","they","not","during","now","him","nor","did","this","she","each","further","where","few","because","doing","some","are","our","ourselves","out","what","for","while","does","above","between","t","be","we","who","were","here","hers","by","on","about","of","against","s","or","own","into","yourself","down","your","from","her","their","there","been","whom","too","themselves","was","until","more","himself","that","but","don","with","than","those","he","me","myself","these","up","will","below","can","theirs","my","and","then","is","am","it","an","as","itself","at","have","in","any","if","again","no","when","same","how","other","which","you","after","most","such","why","a","off","i","yours","so","the","having","once"]

# create Porter stemmer
go_stem = PorterStemmer()

# create tokenizer
tokenizer = RegexpTokenizer(r'[a-z]+')

# create global corpus list
corpus = []

# creating some functions
def create_codebook(docs):
    """intakes list of documents and returns a FreqDist object"""
    global corpus
    all_tokens = []
    for i in docs:
        # convert url to readable raw, lower-case string
        raw = i.lower()
        
        # tokenize raw
        tokens = tokenizer.tokenize(raw)
        
        # remove stop words from tokens
        stopped = [i for i in tokens if not i in go_stop]
        
        # stem tokens
        stemmed = [go_stem.stem(i) for i in stopped]
        
        # add to tokens to total list
        all_tokens = all_tokens + stemmed
    corpus = corpus + all_tokens
    return nltk.FreqDist(all_tokens)
    
def entropy(topic):
    start_time = time.time()
    """returns entropy of codebook_i"""
    e = 0
    for i in topic.keys():
        e += (topic.freq(i) * np.log2(topic.freq(i)))
    print("--- %s seconds ---" % (time.time() - start_time))
    return -e

def cross_entropy(topic_i, topic_j, corp):
    """returns entropy from topic_i to topic_j"""
    e = 0
    start_time = time.time()
    for word in topic_i.keys():
        if word in topic_j.keys():
            e += topic_i.freq(word) * np.log2(topic_j.freq(word))
        else:
            e += topic_i.freq(word) * np.log2(corp.freq(word))
    print("--- %s seconds ---" % (time.time() - start_time))
    return -e

# create dicts for opening txt files
groups = {}
docs = {}

# create topic dict
with open('groups2.txt', 'r') as f:
    next(f)
    csv_reader = csv.reader(f, delimiter='\t')
    for doc_id, topic_id in csv_reader:
        groups[doc_id] = int(topic_id)

# create docs dict and append text by topic
with open('abstracts2.txt', encoding='utf-8') as f:
    next(f)
    csv_reader = csv.reader(f, delimiter='\t')
    for doc_id2, doc_text in csv_reader:
        topic_id = groups[doc_id2]
        try:
            docs[topic_id].append(doc_text)
        except KeyError:
            docs[topic_id] = [doc_text]

# create codebooks for each topic
topic_freq = {key: create_codebook(docs[key]) for key in docs}

# create seperate corpus codebook
corpus_freq = nltk.FreqDist(corpus)

# calculate entropy
topic_shannon = {key: entropy(topic_freq[key]) for key in topic_freq}

# create a matrix for jargon distance calculations
# one cell for each i to j / reader to writer relationship
jarg_matrix = np.zeros((len(topic_freq), len(topic_freq)))

# calculate jargon distance and insert into matrix
for i in topic_freq:
    for j in topic_freq:
        jarg = 1 - (topic_shannon[i] / cross_entropy(topic_freq[i], topic_freq[j], corpus_freq))
        jarg_matrix[i-1, j-1] = jarg

# My jargon distance is coming out negative, which must be incorrect.
abs_matrix = np.absolute(jarg_matrix)

# create dendrogram
distances = (abs_matrix + abs_matrix.T) / 2
clusters = cluster.hierarchy.average(distances)
dendro = plt.figure(figsize=(8,6))
cluster.hierarchy.dendrogram(clusters)
dendro.savefig('dendrogram.png')