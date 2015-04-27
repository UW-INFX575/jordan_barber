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

dir = "https://s3-us-west-2.amazonaws.com/uspto-patentsclaims/"
page_id = ["6334220", "6334221", "6334222", "6334223", "6334224", "6334225", "6334226", "6334227", "6334228", "6334229"]

# initilize lists for loop
all_uni_grams = []
all_bi_grams = []
all_tri_grams = []

for i in page_id:
    # construct url
    url = dir + i + ".txt"
    
    # dump source into page
    page = urllib.request.urlopen(url)
    
    # convert url to readable raw, lower-case string
    raw = page.read()
    raw = raw.decode()
    raw = raw.lower()

    # tokenize raw
    tokens = tokenizer.tokenize(raw)

    # remove stop words from tokens
    stopped = [i for i in tokens if not i in go_stop]

    # stem tokens
    stemmed = [go_stem.stem(i) for i in stopped]
    
    # branch bigram and trigrams into separate lists
    bi_grams = [ " ".join(pair) for pair in nltk.bigrams(stemmed)]
    tri_grams = [ " ".join(pair) for pair in nltk.trigrams(stemmed)]
    
    # add to running total of ngrams for all documents
    all_uni_grams = all_uni_grams + stemmed
    all_bi_grams = all_bi_grams + bi_grams
    all_tri_grams = all_tri_grams + tri_grams
    
    # count frequency of ngrams
    # bi and tri grams use the nltk FreqDist method. Unigram simply uses Counter
    c = Counter(stemmed)
    bi_dist = nltk.FreqDist(bi_grams)
    tri_dist = nltk.FreqDist(tri_grams)
    
    # convert unigrams to dict
    c = dict(c)
    
    # write to csv
    with open('%s_unigrams.csv' % i, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for key, value in c.items():
            writer.writerow([key, value])
    with open('%s_bigrams.csv' % i, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for key, value in bi_dist.items():
            writer.writerow([key, value])
    with open('%s_tigrams.csv' % i, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for key, value in tri_dist.items():
            writer.writerow([key, value])

# count frequency of total ngrams
c = Counter(all_uni_grams)
all_bi_dist = nltk.FreqDist(all_bi_grams)
all_tri_dist = nltk.FreqDist(all_tri_grams)

# convert Counter to dict type
c = dict(c)

# write to csv
with open('total_unigram.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    for key, value in c.items():
        writer.writerow([key, value])
with open('total_bigrams.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    for key, value in all_bi_dist.items():
        writer.writerow([key, value])
with open('total_trigrams.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    for key, value in all_tri_dist.items():
        writer.writerow([key, value])