

__author__ = 'tmwsiy'

import mysql.connector
import os

onet_data = r"C:/Users/tmwsiy/Downloads/db_19_0_mysql/db_19_0_mysql"

connection = mysql.connector.connect(host='localhost', user='root', passwd='password', db='onet_19')
cursor = connection.cursor()
for dirname, dirnames, filenames in os.walk(onet_data):
    for filename in filenames:
        if  filename.endswith(".sql"):
            #print(filename)
            query = "SOURCE " + dirname + '/' + filename
            print(query)
            cursor.execute( query, multi=True )
            connection.commit()




