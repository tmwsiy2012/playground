__author__ = 'tmwsiy'


import urllib2
from urllib2 import urlopen
import re
import cookielib
import json
from cookielib import CookieJar
import time

headers = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')]

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = headers

try:
    page = 'https://btc-e.com/api/2/btc_usd/trades'
    trades = json.loads(opener.open(page).read())
    for trade in trades:
        print trade
except Exception, e:
    print str(e)