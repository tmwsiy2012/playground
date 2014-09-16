import httplib


#host='152.20.244.74'
host='webdev.cislabs.uncw.edu'
conn = httplib.HTTPConnection(host, 8080)
conn.request("GET", "/1003.wakeup")
response = conn.getresponse()
print response.status, response.reason
data = response.read()
print data
conn.close()