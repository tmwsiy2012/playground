__author__ = 'tmwsiy'


import urllib2

import mysql
from urllib2 import urlopen
import re
import cookielib
import json
from cookielib import CookieJar
import time
import pprint
from conf.config import db_config



class MySQLCursorDict(mysql.connector.cursor.MySQLCursorBuffered):
    def _row_to_python(self, rowdata, desc=None):
        row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
        if row:
            return dict(zip(self.column_names, row))
        return None

def insert_trade(trans_data):
    db_conn = mysql.connector.connect(**db_config)
    cursor = db_conn.cursor()
    sql_to_insert = ("INSERT INTO trades (date,price,amount,tid,price_currency,item,trade_type) VALUES (from_unixtime(%s),%s,%s,%s,%s,%s,%s);");
    data_to_insert = (trans_data['date'], trans_data['price'],trans_data['amount'],trans_data['tid'],trans_data['price_currency'],trans_data['item'],trans_data['trade_type'])
    try:
        cursor.execute(sql_to_insert,data_to_insert)
        #id = cursor.lastrowid
        db_conn.commit()
    except Exception,e:
        print e
    finally:
        cursor.close()
        db_conn.close()


def get_last_trans_id(pair):
    return_value = 0
    p1,p2 = pair.split("_")
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(cursor_class=MySQLCursorDict)
    cursor.execute("select max(tid) as last_tid from trades where price_currency=%s AND item=%s",[p2,p1])
    rows = cursor.fetchall()
    for row in rows:
        return_value = row['last_tid']
    return return_value

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

current_milli_time = lambda: int(round(time.time() * 1000))
current_second_time = int(round(time.time()))
#print current_second_time
current_prices = {}
current_millis = current_milli_time()
pairs = {'btc_usd':current_millis,'btc_rur':current_millis,'btc_eur':current_millis,'ltc_btc':current_millis,'ltc_usd':current_millis,'ltc_rur':current_millis,'ltc_eur':current_millis,'nmc_btc':current_millis,'nmc_usd':current_millis,'nvc_btc':current_millis,'nvc_usd':current_millis,'usd_rur':current_millis,'eur_usd':current_millis,'trc_btc':current_millis,'ppc_btc':current_millis,'ftc_btc':current_millis,'xpm_btc':current_millis}
print "pairs: " + str(len(pairs))
while 1:
    for pair in pairs:
        if current_milli_time() > pairs[pair]:
            page = 'https://btc-e.com/api/2/' + pair + '/trades'
            try:
                trade_list = json.loads(opener.open(page).read())
                last_tid = get_last_trans_id(pair)
            except Exception,e:
                print e
                continue

            for trade in trade_list:
                if  trade['tid'] > last_tid:
                    insert_trade(trade)


            first_trade_time = trade_list[len(trade_list) - 1]['date']
            last_trade_time = trade_list[0]['date']
            last_trade_price = trade_list[0]['price']
            current_prices[pair] = float(last_trade_price)
            pairs[pair] = current_milli_time() + (((last_trade_time - first_trade_time) * 1000)/8)
            if pairs[pair]  < 120:
                pairs[pair]  = 120

            d = datetime.timedelta(milliseconds=(pairs[pair]))
            print pair + ": " + str(pairs[pair]) + " Next run time: " + str(d)
            conn.close()
            print "finished " + pair
#        else:
#            d = datetime.datetime.fromtimestamp(pairs[pair]/1000.0)
#            print "not reached next run " + pair +  " Next run time: " + str(d)
    print "finished set waiting..."
    time.sleep(7)