

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
#import json
import simplejson as json
from cookielib import CookieJar
import time
import random
import pprint
from conf.config import db_config
from data.antipool import ConnectionPool


current_second_time = lambda:  int(round(time.time()))
current_seconds = current_second_time() - 1
# Pre-loading data structure with current time for all pairs and the symbolid in the database
#pairs = {'btc_usd':[current_seconds,1,1]}

pairs = {'btc_usd':[current_seconds,1,1,'stopped','high'],'btc_rur':[current_seconds,2,1,'stopped','high'],'btc_eur':[current_seconds,3,1,'stopped','high'],'ltc_btc':[current_seconds,4,1,'stopped','high']
    ,'ltc_usd':[current_seconds,5,1,'stopped','high'],'ltc_rur':[current_seconds,6,1,'stopped','low'],'ltc_eur':[current_seconds,7,1,'stopped','low'],'nmc_btc':[current_seconds,8,1,'stopped','low'],
         'nmc_usd':[current_seconds,9,1,'stopped','low'],'nvc_btc':[current_seconds,10,1,'stopped','low'],'nvc_usd':[current_seconds,11,1,'stopped','low'],'usd_rur':[current_seconds,12,1,'stopped','low']
    ,'eur_usd':[current_seconds,13,1,'stopped','low'],'trc_btc':[current_seconds,14,1,'stopped','low'],'ppc_btc':[current_seconds,15,1,'stopped','low'],'ftc_btc':[current_seconds,16,1,'stopped','low'],'xpm_btc':[current_seconds,17,1,'stopped','high']}

for pair in pairs:
    pairs[pair][0] += random.randint(3, 11)


class MySQLCursorDict(mysql.connector.cursor.MySQLCursorBuffered):
    def _row_to_python(self, rowdata, desc=None):
        row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
        if row:
            return dict(zip(self.column_names, row))
        return None

class BTCETradeUpdater(threading.Thread):
    def __init__(self,priority,id, pair, datavendorid, symbolid, lock):
        super(BTCETradeUpdater, self).__init__()
        self.id = id
        global pairs
        self.lock = lock
        self.pair = pair
        self.page = 'https://btc-e.com/api/2/' + self.pair + '/trades'
        self.priority=priority
        self.next_update = current_second_time() + 3
        self.datavendorid  =datavendorid
        self.symbolid = symbolid
        self.MAX_WAIT_HIGH=5
        self.MAX_WAIT_LOW=45
        self.headers = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')]
        self.cj = CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        self.opener.addheaders = self.headers

    def run(self):
        try:
            trade_list = json.loads(self.opener.open(self.page).read())
            last_tid = self.get_last_trans_id()

            trades_to_insert = []
            for trade in trade_list:
                if trade['tid'] > last_tid:
                    trades_to_insert.append([trade, self.datavendorid, self.symbolid])
            self.insert_trades( trades_to_insert)
            #first_trade_time = trade_list[len(trade_list) - 1]['date']
            first_trade_time = trade_list[49]['date']
            last_trade_time = trade_list[0]['date']
            avg_last_fifty = float((last_trade_time - first_trade_time))/50
            td = int( avg_last_fifty * 10)
            max_wait = 0
            #print str(self.id), self.pair, self.priority
            if self.priority == 'high':
                self.max_wait = self.MAX_WAIT_HIGH
            else:
                self.max_wait = self.MAX_WAIT_LOW
            if td > self.max_wait:
                td = self.max_wait
            #print str(td)
            self.next_update = current_second_time() + td

            now = datetime.datetime.fromtimestamp(current_second_time())
            nxtd = datetime.datetime.fromtimestamp(self.next_update)
            print str(self.id) + "--" + str(now.minute) + ":" + str(now.second) + " " + pair + ": added " + str(len(trades_to_insert)) + " new trades: Next run time in:  " + str(td) + " seconds " + str(nxtd.minute) + ":" + str(nxtd.second)
        except Exception,e:
            print e
        finally:
            self.lock.acquire()
            pairs[pair][0] = self.next_update
            pairs[pair][3] = 'stopped'
            self.lock.release()


    def insert_trades(self,trades_to_insert_struct):
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
                data_to_insert = (self.datavendorid, self.symbolid, td[0]['date'], td[0]['price'], td[0]['amount'], td[0]['tid'],
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


    def get_last_trans_id(self):
        return_value = 0
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(cursor_class=MySQLCursorDict)
        try:
            cursor.execute("select max(tid) as last_tid from price_tradebook where datavendorid=%s AND symbolid=%s",[self.datavendorid,self.symbolid])
            rows = cursor.fetchall()
            for row in rows:
                return_value = row['last_tid']
            return return_value
        except Exception, e:
            print 'get_last_trans_id:',  e
        finally:
            cursor.close()
            connection.close()
thread_list = {}
thr_id =0
lock = threading.Lock()
count = 0
while 1:
    for pair in pairs:
        next_update_time = pairs[pair][0]
        symbolid = pairs[pair][1]
        datavendorid = pairs[pair][2]
        priority = pairs[pair][4]
        lock.acquire()
        if pairs[pair][3] == 'stopped':
            if current_second_time() > next_update_time:
                thr_id += 1
                pairs[pair][3] = 'running:'+str(thr_id)
                t = BTCETradeUpdater(priority,thr_id,pair, datavendorid, symbolid, lock)
                t.start()
                #print 'launched:',thr_id,'pair:',pair
        lock.release()
        time.sleep(0.1)
        count += 1
    if count % 100 == 0:
        print current_second_time(), pairs