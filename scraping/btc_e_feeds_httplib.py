__author__ = 'tmwsiy'

import httplib
import requests

pairs = ['xpm_btc', 'ltc_eur', 'btc_usd', 'ltc_btc', 'nmc_usd', 'ltc_rur', 'nvc_usd', 'eur_usd', 'ltc_usd', 'nvc_btc', 'ftc_btc', 'ppc_btc', 'btc_eur', 'btc_rur', 'usd_rur', 'trc_btc', 'nmc_btc']



conn = httplib.HTTPSConnection('btc-e.com','443')
while True:
    for pair in pairs:
        conn.request('GET', '/api/2/' + pair + '/trades')
        print pair,conn.getresponse().read()