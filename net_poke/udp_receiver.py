import socket
import urllib
import zipfile
import sys, struct, socket
from subprocess import call


# Configuration variables

data_url = "http://www.csc.uncw.edu/mac_lists.zip"
allowed_ips = ['127.0.0.1','152.20.244.74']
listen_port=4239
base_dir = '/home/tmwsiy/'
data_dir = base_dir+'mac_lists/'
broadcast = {'BR':['152.20.223.255'], 'CI':['152.20.234.255']}
wol_port = 9

def wakeup_room(mac_list, building_code):
    for ethernet_address in mac_list:
        wakeup_machine(ethernet_address, building_code)
    return len(mac_list)

def wakeup_machine(ethernet_address, building_code):
    # Construct 6 byte hardware address
    add_oct = ethernet_address.split(':')
    if len(add_oct) != 6:
        print "\n*** Illegal MAC address\n"
        print "MAC should be written as 00:11:22:33:44:55\n"
        return
    hwa = struct.pack('BBBBBB', int(add_oct[0],16),
        int(add_oct[1],16),
        int(add_oct[2],16),
        int(add_oct[3],16),
        int(add_oct[4],16),
        int(add_oct[5],16))

    # Build magic packet

    msg = '\xff' * 6 + hwa * 16

    # Send packet to broadcast address using UDP port 9
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
        for i in broadcast[building_code]:
            soc.sendto(msg,(i,wol_port))
        soc.close()
    except Exception, err:
         print 'problem sending magic packet', Exception, err


def importMacs( room_number):
    return [line.strip() for line in open(data_dir + room_number +".txt")]

def update_data():
    pass


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
            if command.startswith("WAKEUP"):
                print "accepted command:", command, "from", addr
                room_number = command.split(":")[1][2:]
                building_code = command.split(":")[1][:2]
                print 'building code', building_code
                print 'room_number', room_number
                num_attempted = wakeup_room( importMacs( room_number ), building_code)
                print "Attempted:", str(num_attempted), "Room:", room_number
            elif command.startswith("UPDATE"):
                update_data()
            else:
                print 'not understood command:', command

        else:
            print "not allowed"
    except Exception, err:
         print 'problem in main loop', Exception, err












'''
    for tmp_mac in mac_list:
        mac = ':'.join(s.encode('hex') for s in tmp_mac.decode('hex'))
        call(["ether-wake","-i","eth1",mac.upper()])
'''