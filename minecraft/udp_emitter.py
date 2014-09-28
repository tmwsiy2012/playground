__author__ = 'tmwsiy'

import socket
#import ssl
#from dtls import do_patch

#do_patch()

UDP_IP = "192.168.5.12"
#UDP_IP = "192.168.5.17"

UDP_PORT = 4239


MESSAGE='/give tmwsiy_avinu command_block\r\n'
#MESSAGE='UPDATE'



sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

