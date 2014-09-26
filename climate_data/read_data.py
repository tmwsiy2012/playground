__author__ = 'tmwsiy'

import os, glob

listing = glob.glob('*.dly')
for filename in listing:
    print filename
    with open(filename,'r') as in_file:
        for line in in_file:
            print 'station:',line[:11]
            print 'year:',line[11:15]
            print 'month:',line[15:17]
            print 'element:',line[17:21]
            print 'value1:',line[21:26]
            print 'mflag1:',line[26:27]
            print 'qflag1:',line[27:28]
            print 'sflag1:',line[28:29]
            print 'value2:',line[29:35]