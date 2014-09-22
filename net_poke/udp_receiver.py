import socket
import urllib
import zipfile
import sys, struct, socket, tempfile, os, csv, traceback
from subprocess import call


# Configuration variables

data_url = "http://www.csc.uncw.edu/mac_lists.zip"
allowed_ips = ['127.0.0.1','152.20.244.74']
listen_port=4239
response_port=4240

broadcast = {'BR':['152.20.223.255'], 'CI':['152.20.234.255']}
machines_to_wake = {}
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
         print 'Problem sending magic packet...', Exception, err


def update_data():
    global machines_to_wake
    machines_to_wake = {}
    tmp_zip = tempfile.mkdtemp()
    name, hdrs = urllib.urlretrieve(data_url, tmp_zip + '\mac_lists.zip')
    zip = zipfile.ZipFile(name)
    zip.extractall(path=tmp_zip)
    for f in os.listdir(os.path.join(tmp_zip,'mac_lists')):
        with open(os.path.join(tmp_zip,'mac_lists',f), "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            for row in csv_reader:
                if len(row) > 6 and not "Workstation" in row[0]:
                    room = row[0][:6]
                    mac_to_store = ':'.join(s.encode('hex') for s in row[6].decode('hex')).upper()
                    if room in machines_to_wake:
                        machines_to_wake[room].append(mac_to_store)
                    else:
                        machines_to_wake[room] = []
                        machines_to_wake[room].append(mac_to_store)

def send_response(MESSAGE, UDP_IP, UDP_PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

# pre populate data before start
update_data()

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
                print "Accepted Command:", command, "from", addr
                room = command.split(":")[1].strip()
                #room_number = command.split(":")[1][2:]
                building_code = room[:2]
                num_attempted = wakeup_room( machines_to_wake[room], building_code)
                print "Attempted:", str(num_attempted), "Room:", room
                print addr
                send_response("OK... Attempted: " + str(num_attempted) + " Room: " + room, addr[0], response_port)
            elif command.startswith("UPDATE"):
                print "Accepted Command:", command, "from:", addr
                update_data()
                send_response("OK... data updated", addr[0], response_port)
            else:
                print 'invalid command:', command, "from:", addr
                send_response("Command not understood", addr[0], response_port)
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