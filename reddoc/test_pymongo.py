__author__ = 'tmwsiy'
import pymongo
import pprint

# Connection to Mongo DB
conn = None
try:
    conn=pymongo.MongoClient()
    print ("Connected successfully!!!")
except pymongo.errors.ConnectionFailure as e:
   print("Could not connect to MongoDB: " + e)

db = conn.corpus
print(db)

for i in db.lemmas.find():
    for j in i['lemmas']:
        if '401' in j['manuscripts']:
            pprint.pprint(j['text'])

#for i in db.lemmas.find():
#    pprint.pprint(i)

#for i in db.lemmas.find( { "chapter":"1"}  ):
#        print( i)

#for i in db.lemmas.find( { "lemmas.manuscripts":"104"}  ):
#    pprint.pprint( i)
