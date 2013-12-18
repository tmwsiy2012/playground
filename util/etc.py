__author__ = 'tmwsiy'
import os, sys

def get_next_nonce():
    os.chdir("../util")
    with open("nonce.txt","r+") as f:
        last_nonce = int(f.read())
        f.seek(0)
        f.truncate()
        next_nonce = last_nonce + 1
        f.write(str(next_nonce))
        return next_nonce

