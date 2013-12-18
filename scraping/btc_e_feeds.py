

__author__ = 'tmwsiy'


import urllib2
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



class MySQLCursorDict(mysql.connector.cursor.MySQLCursorBuffered):
    def _row_to_python(self, rowdata, desc=None):
        row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
        if row:
            return dict(zip(self.column_names, row))
        return None

def insert_trades(trades_to_insert_struct):
    datavendorid=trades_to_insert_struct[1]
    symbolid=trades_to_insert_struct[2]
    trades_to_insert=trades_to_insert_struct[0]
    try:
        db_conn = mysql.connector.connect(**db_config)
        cursor = db_conn.cursor()
        sql_to_insert = ("INSERT INTO price_tradebook (datavendorid,symbolid,price_date,price,amount,tid,price_currency,item,trade_type) VALUES (%s,%s,from_unixtime(%s),%s,%s,%s,%s,%s,%s);");
        for trans_data in trades_to_insert:
            print trans_data['price']
            data_to_insert = (datavendorid,symbolid,trans_data['date'], trans_data['price'],trans_data['amount'],trans_data['tid'],trans_data['price_currency'],trans_data['item'],trans_data['trade_type'])
            cursor.execute(sql_to_insert,data_to_insert)
            #id = cursor.lastrowid
        db_conn.commit()
    except Exception,e:
        print 'insert_trades:',e
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

headers = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')]

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = headers

datavendorid=1
current_milli_time = lambda: int(round(time.time() * 1000))
current_second_time = int(round(time.time()))
#print current_second_time
current_prices = {}
current_millis = current_milli_time()
pairs = {'btc_usd':[current_millis,1],'btc_rur':[current_millis,2],'btc_eur':[current_millis,3],'ltc_btc':[current_millis,4]
    ,'ltc_usd':[current_millis,5],'ltc_rur':[current_millis,6],'ltc_eur':[current_millis,7],'nmc_btc':[current_millis,8],
         'nmc_usd':[current_millis,9],'nvc_btc':[current_millis,10],'nvc_usd':[current_millis,11],'usd_rur':[current_millis,12]
    ,'eur_usd':[current_millis,13],'trc_btc':[current_millis,14],'ppc_btc':[current_millis,15],'ftc_btc':[current_millis,16],'xpm_btc':[current_millis,17]}
print "pairs: " + str(len(pairs))
while 1:
    for pair in pairs:
        next_update_time = pairs[pair][0]
        symbolid=pairs[pair][1]
        if current_milli_time() > next_update_time:
            page = 'https://btc-e.com/api/2/' + pair + '/trades'
            try:
                trade_list = json.loads(opener.open(page).read())
                last_tid = get_last_trans_id(datavendorid,symbolid)
                last_tid = get_last_trans_id(datavendorid,symbolid)
            except Exception,e:
                print e
                continue
            trades_to_insert = []
            for trade in trade_list:
                if  trade['tid'] > last_tid:
                    trades_to_insert.append([trade,datavendorid,symbolid])

            print len(trades_to_insert)
            insert_trades(trades_to_insert)

            first_trade_time = trade_list[len(trade_list) - 1]['date']
            last_trade_time = trade_list[0]['date']
            last_trade_price = trade_list[0]['price']
            current_prices[pair] = float(last_trade_price)
            next_update_time = current_milli_time() + (((last_trade_time - first_trade_time) * 1000)/8)
            if next_update_time  < 120:
                next_update_time  = 120

            d = timedelta(milliseconds=(next_update_time))
            print pair + ": " + str(next_update_time) + " Next run time: " + str(d)
            print "finished " + pair
#        else:
#            d = datetime.datetime.fromtimestamp(pairs[pair]/1000.0)
#            print "not reached next run " + pair +  " Next run time: " + str(d)
    print "finished set waiting..."
    time.sleep(7)