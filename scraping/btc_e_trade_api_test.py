# If you find this sample useful, please feel free to donate :)
# LTC: LePiC6JKohb7w6PdFL2KDV1VoZJPFwqXgY
# BTC: 1BzHpzqEVKjDQNCqV67Ju4dYL68aR8jTEe

import httplib
import urllib
import json
import hashlib
import hmac
import pprint
from util.etc import get_next_nonce
from conf.config import BTCE_api_secret,BTCE_api_key

# Replace these with your own API key data

# Come up with your own method for choosing an incrementing nonce
nonce = get_next_nonce()

# method name and nonce go into the POST parameters
params = {"method":"TradeHistory",
          "nonce": nonce}
params = urllib.urlencode(params)

# Hash the params string to produce the Sign header value
H = hmac.new(BTCE_api_secret, digestmod=hashlib.sha512)
H.update(params)
sign = H.hexdigest()

headers = {"Content-type": "application/x-www-form-urlencoded",
           "Key":BTCE_api_key,
           "Sign":sign}
conn = httplib.HTTPSConnection("btc-e.com")
conn.request("POST", "/tapi", params, headers)
response = conn.getresponse()

pp = pprint.PrettyPrinter(indent=3)
print response.status, response.reason
pp.pprint(json.load(response))

conn.close()