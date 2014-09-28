import socket
import urllib
import zipfile
import sys, struct, socket, tempfile, os, csv, traceback
from threading import Thread

import subprocess


# Configuration variables


allowed_ips = ['127.0.0.1','192.168.5.17']
listen_port=4239
server_executable='./jre1.7.0_67/bin/java -Xmx1024M -Xms1024M -jar ./minecraft_server.1.8.jar nogui'

def print_output( stdout_pipe):
    while True:
        proc_read = stdout_pipe.readline()
        print proc_read


proc = subprocess.Popen(server_executable,
                        shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)

tmp_str = proc.stdout.readline()
while 'Done' not in tmp_str:
    print tmp_str
    tmp_str = proc.stdout.readline()
print tmp_str

t = Thread(target=print_output, args=(proc.stdout,))
t.start()

sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
sock.bind(('', listen_port))

while True:
    print "waiting for data..."
    try:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        if not data:
            break;
        if addr[0] in allowed_ips:
            command = str(data)
            print command
            proc.stdin.write(command)
            proc.stdin.flush()

        else:
            print "NOT ALLOWED payload:", str(data), "from:", addr
    except Exception, err:
        traceback.print_exc()
        print 'problem in main loop', Exception, err












'''
    for tmp_mac in mac_list:
        mac = ':'.join(s.encode('hex') for s in tmp_mac.decode('hex'))
        call(["ether-wake","-i","eth1",mac.upper()])
'''