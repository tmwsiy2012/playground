__author__ = 'tmwsiy'

import zmq
import random
import time

context = zmq.Context()

# Socket to send messages on
sender = context.socket(zmq.PUSH)
sender.bind("tcp://*:5557")

# Socket with direct access to the sink: used to syncronize start of batch
sink = context.socket(zmq.PUSH)
sink.connect("tcp://localhost:5558")

#print "Press Enter when the workers are ready: "
#_ = raw_input()
#print "Sending tasks to workers..."

# The first message is "0" and signals start of batch
sink.send('0')

# Initialize random number generator
random.seed()

pairs = {'btc_usd',
         'btc_rur',
         'btc_eur',
         'ltc_btc',
         'ltc_usd',
         'ltc_rur',
         'ltc_eur',
         'nmc_btc',
         'nmc_usd',
         'nvc_btc',
         'nvc_usd',
         'usd_rur',
         'eur_usd',
         'trc_btc',
         'ppc_btc',
         'ftc_btc',
         'xpm_btc'}

pairs_ids = {'btc_usd':'1,1',
         'btc_rur':'2,1,',
         'btc_eur':'3,1,',
         'ltc_btc':'4,1'
    ,   'ltc_usd':'5,1',
         'ltc_rur':'6,1',
         'ltc_eur':'7,1',
         'nmc_btc':'8,1',
         'nmc_usd':'9,1',
         'nvc_btc':'10,1',
         'nvc_usd':'11,1',
         'usd_rur':'12,1',
         'eur_usd':'13,1',
         'trc_btc':'14,1',
         'ppc_btc':'15,1',
         'ftc_btc':'16,1',
         'xpm_btc':'17,1'}


# send out initial
while True:
    for pair in pairs:
        sender.send(pair + "," + pairs_ids[pair] )
    time.sleep(60)
# Give 0MQ time to deliver
