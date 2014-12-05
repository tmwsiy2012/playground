__author__ = 'tmwsiy'

import pymongo
import nltk
import tfidf
from nltk.corpus import stopwords
import cPickle as pickle
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
collection = db.sightings_geo


tokens= []
documents=[]
global_doc={}
results={}

for post in collection.find():
    id = str(post['_id'])
    documents.append(id)

'''
stopset= set(stopwords.words('english'))
table = tfidf.tfidf()
counter=0
for post in collection.find():
    counter = counter + 1
    if counter % 10000 == 0:
        print counter
    tmp_tokens= nltk.word_tokenize(post['description'].lower())
    id = str(post['_id'])
    documents.append(id)
    doc_tokens = []
    for t in tmp_tokens:
        if t not in stopset:
            doc_tokens.append(t)
    #print doc_tokens
    table.addDocument(id, doc_tokens)
    global_doc[id]= doc_tokens

pickle.dump( table, open( "table.p", "wb" ) )
print 'finished tokenizing'
'''

corpus = pickle.load( open( "table.p", "rb" ) )
counter=0

for id in documents:
    counter = counter + 1
    print counter
    results[id]= corpus.similarities(global_doc[id])

#print results
pickle.dump( results, open( "similarities.p", "wb" ) )



'''
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
'''