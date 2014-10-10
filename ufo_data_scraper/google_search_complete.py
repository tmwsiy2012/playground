__author__ = 'tmwsiy'

import requests, json
from urllib import quote

#http://www.google.com/complete/search?hl=en&js=true&qu=sugge

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
}
tld= 'com'
lang='en'
query= quote('Pompono bck, FL'.encode('utf-8') )
ds=''

url = "http://clients1.google.%s/complete/search?hl=%s&q=%s&json=t&ds=%s&client=serp" %(tld, lang, query, ds)
print url
response = requests.get(url,timeout=10, headers=headers)
result = json.loads(response.content)
suggestions = [i for i in result[1]]
print suggestions
