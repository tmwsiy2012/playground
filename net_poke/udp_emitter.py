__author__ = 'tmwsiy'

import socket
#import ssl
#from dtls import do_patch

#do_patch()

UDP_IP = "127.0.0.1"

UDP_PORT = 4239
listen_port=4240

MESSAGE='WAKEUP:CI1003'
#MESSAGE='UPDATE'

reply_socket = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
reply_socket.bind(('', listen_port))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

data, addr = reply_socket.recvfrom(1024) # buffer size is 1024 bytes
print "received:", data, "from", addr
