__author__ = 'tmwsiy'

import pymongo, re
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


#db.sightings.remove({"occurred" : {'$regex' : "^2\/[0-9]{1,2}\/2014.*"}})

results = db.sightings.find({"occurred" : {'$regex' : "^2\/[0-9]{1,2}\/2014.*"}})

for result in results:
    print result['description']
    re.findall(r'[a-z]{1}[A-Z]{1}', result['description'])


