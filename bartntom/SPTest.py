import mysql.connector


connection = mysql.connector.connect(host='localhost', user='root', passwd='tr45sh32', db='bls_qcew')
cursor = connection.cursor()
cursor.callproc("get_annual_entries_by_area_code",['C4870','2012'])
#results = cursor.fetchall
for result in cursor.stored_results():
    results=result.fetchall()

for row in results:
    print(row[0])
