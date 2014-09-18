from urllib import addbase

__author__ = 'tmwsiy'

import netifaces


#print netifaces.ifaddresses('em1')
'''
from netifaces import interfaces, ifaddresses, AF_INET
for ifaceName in interfaces():
    print ifaceName
    addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
    print '%s: %s' % (ifaceName, ', '.join(addresses))


'''
for iface in netifaces.interfaces():
    for address in netifaces.ifaddresses(iface):
        ip_dict =  netifaces.ifaddresses(iface)[address][0]
        if 'broadcast' in ip_dict and ip_dict['broadcast'].startswith('152.20'):
            print ip_dict['broadcast']

