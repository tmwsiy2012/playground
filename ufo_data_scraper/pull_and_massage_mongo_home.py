__author__ = 'tmwsiy'

import pymongo, re
from dateutil.parser import parse
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
    if 'description' in post:
        #print '\n\n'
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
        m = re.search('\(\((NUFORC Note:.*\))\)',new_description)
        if m:
            print m.group(0)
        #print 'count:', str(count),'\n', new_description
        try:
            new_document['description']=new_description
            new_document['occurred']= parse(post['occurred'].split('(')[0].strip())
            new_document['reported']= parse(post['reported'].split('M')[0] + 'M')
            new_document['posted']= parse(post['posted'].strip())
            new_document['location']= post['location'].strip()
            new_document['shape']= post['shape'].strip()
            new_document['duration']= post['duration']
            local_collection.insert(new_document)
        except Exception,e:
            print str(e)
            print 'post[\'reported\']', post['reported']
            print 'post[\'occurred\']',post['occurred']
            print 'post[\'posted\']',post['posted']


#re.finditer(pattern, string[, flags])