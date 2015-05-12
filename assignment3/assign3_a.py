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

# create stopper for english words
go_stop = get_stop_words('en')

# create Porter stemmer
go_stem = PorterStemmer()

# create tokenizer using regex \w+ method
tokenizer = RegexpTokenizer(r'\w+')

# create sample documents
# topic A
doc_a = "Brocolli is good to eat. My brother likes to eat good brocolli, but not my mother."
doc_b = "Some health experts suggest that driving may cause increased tension and blood pressure."
doc_c = "Health professionals say that brocolli is good for your health."

# topic B
doc_d = "My mother spends a lot of time driving my brother around to baseball practice."
doc_f = "I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better."

# compile sample documents into two topics and a corpus
topic_a = [doc_a, doc_b, doc_c]
topic_b = [doc_d, doc_f]
corpus = [doc_a, doc_b, doc_c, doc_d, doc_f]

def create_codebook(tokenlist):
    """intake a list of documents and create a codebook"""
    all_tokens = []
    for i in tokenlist:
        # convert url to readable raw, lower-case string
        raw = i.lower()
        
        # tokenize raw
        tokens = tokenizer.tokenize(raw)
        
        # remove stop words from tokens
        stopped = [i for i in tokens if not i in go_stop]
        
        # stem tokens
        stemmed = [go_stem.stem(i) for i in stopped]
        
        # add to tokens for all documents
        all_tokens = all_tokens + stemmed
    return nltk.FreqDist(all_tokens)

def cross_entropy(termprob, corpusprob):
    """calculate cross entropy"""
    return -(termprob * math.log(corpusprob, 2))
    
def shannon_entropy(termprob):
    """calculate shannon entropy"""
    return -(termprob * math.log(termprob, 2))

# create codebooks for topics A, B, and the corpus codebook
# includes distribution frequency, phrase counts, etc.
a_codebook = create_codebook(topic_a)
b_codebook = create_codebook(topic_b)
corp_codebook = create_codebook(corpus)

# calculate shannon entropy for each phrase in topic a
shannon_topic_a = []
for i in a_codebook:
    shannon_topic_a.append(shannon_entropy(a_codebook.freq(i)))

# calculate cross entropy for each phrase in topic a
cross_topic_a = []
for i in a_codebook:
    if b_codebook.freq(i) == 0.0:
        # if term does not exist in topic b, refer to corpus codebook
        cross_topic_a.append((cross_entropy(a_codebook.freq(i), corp_codebook.freq(i))))
    else:
        # refer to topic b codebook
        cross_topic_a.append((cross_entropy(a_codebook.freq(i), b_codebook.freq(i))))

# average message length within topic a
avg_msg_within = mean(shannon_topic_a)

# average message length between topic a to b
avg_msg_between = mean(cross_topic_a)

# calculate efficiency of communication between topic a to b
cultural_hole_a_to_b = avg_msg_within / avg_msg_between

# cultural hold from reader in topic b to topic a
cultural_hole_b_to_a = 1 - cultural_hole_a_to_b

# calculate average cultural hole around topic a, n=2
avg_cultural_hole = cultural_hole_a_to_b / 2
