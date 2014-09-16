#Copyright Jon Berg , turtlemeat.com

import string,cgi,time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from subprocess import call
#import pri

allowed = ['127.0.0.1','152.20.244.74']
listen_port=4239


def wakeup_room(mac_list):
    for tmp_mac in mac_list:
        mac = ':'.join(s.encode('hex') for s in tmp_mac.decode('hex'))
        print mac.upper()
        call(["ether-wake","-i","eth1",mac.upper()])

def importMac( room_number):
    allmacs = []

    allmacs = [line.strip() for line in open("/home/tmwsiy/"+ room_number +".txt")]

    return allmacs


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.client_address[0] in allowed:
                if self.path.endswith(".wakeup"):   #our dynamic content
                    req = self.path.split('.')
                    room =  req[0][1:]
                    print room
                    self.send_response(200)
                    self.send_header('Content-type',	'text/html')
                    self.end_headers()
                    self.wfile.write("OK, waking up room: " + room)
                    wakeup_room( importMac( room))
                    return

                return
            else:
                self.send_response(200)
                self.send_header('Content-type',	'text/html')
                self.end_headers()
                self.wfile.write("Unauthorized Address")

                
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
     

    def do_POST(self):
        global rootnode

        try:
            self.wfile.write("Unimplemented Verb")
            
        except :
            pass

def main():
    try:
        server = HTTPServer(('', listen_port), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

