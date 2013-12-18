__author__ = 'tmwsiy'


import urllib2

import mysql
from urllib2 import urlopen
import re
import cookielib
import json
from cookielib import CookieJar
import time



class MySQLCursorDict(mysql.connector.cursor.MySQLCursorBuffered):
    def _row_to_python(self, rowdata, desc=None):
        row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
        if row:
            return dict(zip(self.column_names, row))
        return None

def insert_trade(trans_data):
    db_conn = mysql.connector.connect(**config)
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
    connection = mysql.connector.connect(**config)
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