__author__ = 'tmwsiy'

import requests, time
import bs4

url_prefix='https://web.archive.org/web/20140824090651/'
current_doc={}
response = requests.get(url_prefix+'http://www.nuforc.org/webreports/ndxevent.html')
time.sleep(1)
for chunk in response.text.split(">"):
    if chunk.endswith(".html") and not "HREF" in chunk[-15:]:
        print chunk[-15:]
