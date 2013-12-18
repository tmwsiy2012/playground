__author__ = 'tmwsiy'

import urllib2
from urllib2 import urlopen
import re
import cookielib
import json
from cookielib import CookieJar
import time

headers = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'),
('Accept','application/json, text/javascript, */*; q=0.01'),
    ('Referer','http://bitcoincharts.com/charts/mtgoxUSD')]

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = headers


def get_bitcoincharts_historical_data(exchange, fiat, days, sampling_frequency):
    """
    Gets data from the bitcoincharts.com
    usage example: get_historical_data('mtgox','180','USD','Daily') (gets 6 months of daily data
    possible frequencies: 'auto','1-min','5-min','15-min','30-min','Hourly','2-hour','6-hour','12-hour','Daily','Weekly'
    returns [[timestamp,open,high,low,close,volume(BTC),volume(fiat),weighted average]...]
    """
    try:
        page = 'http://bitcoincharts.com/charts/chart.json?m=' + exchange + fiat + '&SubmitButton=Draw&r=' + days + '&i=' + sampling_frequency + '&c=0&s=&e=&Prev=&Next=&t=S&b=&a1=&m1=10&a2=&m2=25&x=0&i1=&i2=&i3=&i4=&v=1&cv=0&ps=0&l=0&p=0&'
        return json.loads(opener.open(page).read())
    except Exception, e:
        print str(e)

def main():
    try:
        entries = get_bitcoincharts_historical_data('mtgox','USD','2280','6-hour')
        for entry in entries:
            try:
                print entry
                timestamp = int(entry[0])
                open_price = float(entry[1])
                high_price = float(entry[2])
                low_price = float(entry[3])
                close_price = float(entry[4])
                volume_btc = float(entry[5])
                volume_fiat = float(entry[6])
                weighted_average = float(entry[7])
            except Exception,e:
                print str(e)
    except Exception, e:
        print str(e)

main()