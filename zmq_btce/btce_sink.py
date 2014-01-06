__author__ = 'tmwsiy'


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
    #sys.stdout.write(s)
    data_to_insert = json.loads( s )

    for trade in data_to_insert[1]:
        sys.stdout.write(str(trade) + '\n')
    sys.stdout.flush()
'''
    last_trans_id=0
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(cursor_class=MySQLCursorDict)
        connection.start_transaction()

        cursor.execute("select max(tid) as last_tid from price_tradebook where datavendorid=%s AND symbolid=%s",[self.datavendorid,self.symbolid])
        rows = cursor.fetchall()
        for row in rows:
            last_trans_id = row['last_tid']


        connection.commit()
    except Exception, e:
        connection.rollback()
        print 'error getting last_trans_id:',  e
    finally:
        cursor.close()
        connection.close()
'''


