__author__ = 'tmwsiy'

import pymongo
from bson import json_util
import json
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

for doc in collection.find({ "$where": "this.reported < this.occurred" } ):
    #reported = json.loads(doc['reported'], object_hook=json_util.object_hook)
    #occurred = json.loads(doc['occurred'], object_hook=json_util.object_hook)
    print 'reported', str(doc['reported']), doc['location']
    print 'occurred', str(doc['occurred']), doc['location']
#print(db)

