__author__ = 'tmwsiy'


import pymongo

remote_conn = None
local_conn = None
try:
    #remote_conn= pymongo.MongoClient(host='152.20.244.74')
    remote_conn= pymongo.MongoClient(host='127.0.0.1',port=27018)
    local_conn= pymongo.MongoClient()
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure as e:
   print "Could not connect to MongoDB: " + str(e)


remote_db = remote_conn.corpus
remote_collection = remote_db.sightings
local_db = local_conn.corpus
local_collection = local_db.sightings_geo
local_collection.remove()
count=0
for post in remote_collection.find():
    count += 1
    if count % 5000 == 0:
        print 'processed', str(count), 'records'
    local_collection.insert(post)