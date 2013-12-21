

__author__ = 'tmwsiy'


import urllib2
import datetime
import Queue
import threading
from datetime import timedelta
import mysql.connector
from urllib2 import urlopen
import re
import cookielib
import json
from cookielib import CookieJar
import time
import pprint
from conf.config import db_config

DATAVENDORID = 1
MAX_WAIT=45
current_second_time = lambda:  int(round(time.time()))
current_seconds = current_second_time()
# Pre-loading data structure with current time for all pairs and the symbolid in the database
pairs = {'btc_usd':[current_seconds,1],'btc_rur':[current_seconds,2],'btc_eur':[current_seconds,3],'ltc_btc':[current_seconds,4]
    ,'ltc_usd':[current_seconds,5],'ltc_rur':[current_seconds,6],'ltc_eur':[current_seconds,7],'nmc_btc':[current_seconds,8],
         'nmc_usd':[current_seconds,9],'nvc_btc':[current_seconds,10],'nvc_usd':[current_seconds,11],'usd_rur':[current_seconds,12]
    ,'eur_usd':[current_seconds,13],'trc_btc':[current_seconds,14],'ppc_btc':[current_seconds,15],'ftc_btc':[current_seconds,16],'xpm_btc':[current_seconds,17]}

headers = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')]
cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = headers


class MySQLCursorDict(mysql.connector.cursor.MySQLCursorBuffered):
    def _row_to_python(self, rowdata, desc=None):
        row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
        if row:
            return dict(zip(self.column_names, row))
        return None


def update_pair(pair_to_fetch, symbolid_to_fetch):
    page = 'https://btc-e.com/api/2/' + pair_to_fetch + '/trades'
    try:
        trade_list = json.loads(opener.open(page).read())
        last_tid = get_last_trans_id(DATAVENDORID, symbolid_to_fetch)
    except Exception,e:
        print e
        return
    trades_to_insert = []
    for trade in trade_list:
        if trade['tid'] > last_tid:
            trades_to_insert.append([trade, DATAVENDORID, symbolid_to_fetch])
    insert_trades(trades_to_insert)
    #first_trade_time = trade_list[len(trade_list) - 1]['date']
    first_trade_time = trade_list[49]['date']
    last_trade_time = trade_list[0]['date']
    avg_last_fifty = float((last_trade_time - first_trade_time))/50
    td = int( avg_last_fifty * 10)
    if td > MAX_WAIT:
        td = MAX_WAIT
    next_update = current_second_time() + td
    pairs[pair][0] = next_update
    print pair + ": added " + str(len(trades_to_insert)) + " new trades: Next run time in:  " + str(td) + " seconds " + str(datetime.datetime.fromtimestamp(next_update))
    return

def insert_trades(trades_to_insert_struct):
    """
    trades_to_insert is a [{},int,int]
    """
    db_conn = mysql.connector.connect(**db_config)
    cursor = db_conn.cursor()
    data_to_insert = []
    try:

        sql_to_insert = ("INSERT INTO price_tradebook (datavendorid,symbolid,price_date,price,amount,tid,price_currency,"
                         "item,trade_type) VALUES (%s,%s,from_unixtime(%s),%s,%s,%s,%s,%s,%s)")
        data_to_insert = ()
        for td in trades_to_insert_struct:
            data_to_insert = (td[1], td[2], td[0]['date'], td[0]['price'], td[0]['amount'], td[0]['tid'],
                              td[0]['price_currency'], td[0]['item'], td[0]['trade_type'])
            #data_to_insert.append((td[1], td[2], td[0]['date'], td[0]['price'], td[0]['amount'], td[0]['tid'],
            #                  td[0]['price_currency'], td[0]['item'], td[0]['trade_type']))
            cursor.execute(sql_to_insert, data_to_insert)
            db_conn.commit()
            #id = cursor.lastrowid
        #cursor.executemany(sql_to_insert, data_to_insert)
        #db_conn.commit()
    except Exception, e:
        print 'insert_trades:', str(data_to_insert), e
    finally:
        cursor.close()
        db_conn.close()


def get_last_trans_id(datavendorid,symbolid):
    return_value = 0
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(cursor_class=MySQLCursorDict)
    cursor.execute("select max(tid) as last_tid from price_tradebook where datavendorid=%s AND symbolid=%s",[datavendorid,symbolid])
    rows = cursor.fetchall()
    for row in rows:
        return_value = row['last_tid']
    return return_value

while 1:
    for pair in pairs:
        next_update_time = pairs[pair][0]
        symbolid=pairs[pair][1]
        if current_second_time() > next_update_time:
            update_pair(pair, symbolid)
