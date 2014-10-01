import json
import urllib

api_key = open(".apikey").read()
service_url = 'https://www.googleapis.com/freebase/v1/mqlread'
query = [{'id': None, 'name': None, 'type': '/meteorology/tropical_cyclone', 'limit': 1385}]
params = {
        'query': json.dumps(query),
        'key': api_key
}
url = service_url + '?' + urllib.urlencode(params)
response = json.loads(urllib.urlopen(url).read())
#print response
for planet in response['result']:
    if planet['id'].startswith('/en/hurricane'):
        query1 = [{'id': planet['id'], 'type': '/meteorology/tropical_cyclone', 'limit': 1}]
        params1 = {
                'query': json.dumps(query),
                'key': api_key
        }
        url1 = service_url + '?' + urllib.urlencode(params1)
        response1 = json.loads(urllib.urlopen(url1).read())
        print response1
        #for planet1 in response1['result']:
        #    print planet['id']