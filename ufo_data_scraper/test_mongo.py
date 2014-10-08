__author__ = 'tmwsiy'

import pymongo, re
import pprint
from collections import OrderedDict

# Connection to Mongo DB
remote_conn = None
local_conn = None
try:
    remote_conn= pymongo.MongoClient(host='152.20.244.74')
    local_conn= pymongo.MongoClient()
    print ("Connected successfully!!!")
except pymongo.errors.ConnectionFailure as e:
   print("Could not connect to MongoDB: " + e)

remote_db = remote_conn.corpus
remote_collection = remote_db.sightings
local_db = local_conn.corpus
local_collection = local_db.sightings
for post in remote_collection.find():
    print '\n\n'
    new_document= {}
    new_description = ''
    #print 'new', post['description']
    indexes = [(m.start(0), m.end(0)) for m in re.finditer('[a-z\.{1,3}][A-Z]', post['description'])]
    count=0
    prev_end=0
    for index in indexes:
        new_description = new_description + post['description'][prev_end:index[0]+1] + ' '
        prev_end= index[1]-1
        count += 1
    new_description = new_description + post['description'][prev_end:]
    #print 'count:', str(count),'\n', new_description




#re.finditer(pattern, string[, flags])