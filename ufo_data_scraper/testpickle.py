__author__ = 'tmwsiy'

import cPickle as pickle

corpus = pickle.load( open( "save1.p", "rb" ) )

for doc in corpus:
    print doc

