__author__ = 'tmwsiy'

import traceback
import sys
import time
import zmq
import simplejson as json
import mysql.connector
from conf.config import db_config




class MySQLCursorDict(mysql.connector.cursor.MySQLCursorBuffered):
    def _row_to_python(self, rowdata, desc=None):
        row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
        if row:
            return dict(zip(self.column_names, row))
        return None

context = zmq.Context()

# Socket to receive messages on
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:5558")

# Wait for start of batch
s = receiver.recv()

task_nbr=0
while True:

    s = receiver.recv_string()

    wire_data = json.loads( s )
    job_params = []
    trades_to_insert = []
    datavendorid = 0
    symbolid = 0
    symbol = ''
    for key in wire_data[0]:
        vals = wire_data[0][key].split(',')
        symbol = key
        datavendorid = int(vals[1])
        symbolidid = int(vals[0])

    last_trans_id=0
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(cursor_class=MySQLCursorDict)
        connection.start_transaction()

        cursor.execute("select max(tid) as last_tid from price_tradebook where datavendorid=%s AND symbolid=%s",[datavendorid,symbolid])
        rows = cursor.fetchall()
        for row in rows:
            last_trans_id = row['last_tid']



        for trade in wire_data[1]:
            if int(trade['tid']) > last_trans_id:
                trades_to_insert.append([trade, datavendorid, symbolid])

        sql_to_insert = ("INSERT INTO price_tradebook (datavendorid,symbolid,price_date,price,amount,tid,price_currency,"
                         "item,trade_type) VALUES (%s,%s,from_unixtime(%s),%s,%s,%s,%s,%s,%s)")
        data_to_insert = ()

        for td in trades_to_insert:
            data_to_insert = ( datavendorid, symbolid, td[0]['date'], td[0]['price'], td[0]['amount'], td[0]['tid'],
                              td[0]['price_currency'], td[0]['item'], td[0]['trade_type'])
            cursor.execute(sql_to_insert, data_to_insert)

        connection.commit()
        sys.stdout.write('finished: ' + key + ' updated: ' + str(len(trades_to_insert)) + '\n')
        sys.stdout.flush()
    except Exception, e:
        connection.rollback()
        traceback.print_exc()
        print 'error getting last_trans_id:',  e
    finally:
        cursor.close()
        connection.close()




