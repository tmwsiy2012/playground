__author__ = 'tmwsiy'

import socket
#import ssl
#from dtls import do_patch

#do_patch()

UDP_IP = "127.0.0.1"

UDP_PORT = 4239

#MESSAGE='WAKEUP:CI1003'
MESSAGE='UPDATE'


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))