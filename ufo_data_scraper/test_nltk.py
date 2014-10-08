__author__ = 'tmwsiy'

import pymongo
import nltk
from nltk import FreqDist
from nltk.util import ngrams
# Connection to Mongo DB
conn = None
try:
    conn=pymongo.MongoClient()
    print ("Connected successfully!!!")
except pymongo.errors.ConnectionFailure as e:
   print("Could not connect to MongoDB: " + e)

db = conn.corpus
collection = db.sightings


tokens= []
for post in collection.find():
    tokens.extend(nltk.word_tokenize(post['description'].lower()))
text = nltk.Text(tokens)
fd = nltk.FreqDist(text)
print 'triangle', fd['triangle']
print 'chevron', fd['chevron']
print 'silent', fd['silent']
print 'blue', fd['blue']
print 'red', fd['red']
print 'green', fd['green']
print 'orange', fd['orange']
print 'purple', fd['purple']
print 'military', fd['military']

fd.plot(100,cumulative=False)


    #print fdist
    #n = 6
    #sixgrams = ngrams(post['description'].split(), n)
    #for grams in sixgrams:
    #    print
    #print post
