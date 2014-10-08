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
collection = db.sightings

print(db)
