__author__ = 'tmwsiy'

import urllib2
from urllib2 import urlopen
import re
import cookielib
from ghost import ghost
from cookielib import CookieJar
import time

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-Agent','Mozilla/5.0')]


def main():
    try:
        page = 'http://bitcoincharts.com/charts/mtgoxUSD#igDailyztgSzm1g10zm2g25zv'
        page_source = opener.open(page).read()
        #print page_source
        options = re.findall(r'<option.*?>(.*?)</option>',page_source)
        for option in options:
            p = re.compile('.*?[A-Z][A-Z][A-Z]$')
            m = p.match(option)
            if m:
                print option
    except Exception,e:
        print(str(e))

main()