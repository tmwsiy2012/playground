__author__ = 'tmwsiy'
import pymongo
import pprint
from collections import OrderedDict

# Connection to Mongo DB
conn = None
try:
    conn=pymongo.MongoClient()
    print ("Connected successfully!!!")
except pymongo.errors.ConnectionFailure as e:
   print("Could not connect to MongoDB: " + e)

db = conn.corpus
print(db)

unique_manuscripts = {}
for i in db.lemmas.find():
    for j in i['lemmas']:
        for k in j['manuscripts']:
            if k in unique_manuscripts:
                unique_manuscripts[k] += 1
            else:
                unique_manuscripts[k] = 1

ordered_unique = OrderedDict(sorted(unique_manuscripts.items(), key=lambda t: t[0]))
pprint.pprint(ordered_unique)


#for i in db.lemmas.find():
#    for j in i['lemmas']:
#        if '401' in j['manuscripts']:
#            pprint.pprint(j['text'])

#for i in db.lemmas.find():
#    pprint.pprint(i)

#for i in db.lemmas.find( { "chapter":"1"}  ):
#        print( i)

#for i in db.lemmas.find( { "lemmas.manuscripts":"104"}  ):
#    pprint.pprint( i)
