__author__ = 'tmwsiy'

import tfidf

table = tfidf.tfidf()
table.addDocument("foo", ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel"])
table.addDocument("bar", ["alpha", "bravo", "charlie", "india", "juliet", "kilo"])
table.addDocument("baz", ["kilo", "lima", "mike", "november"])

print table.similarities (["alpha", "bravo", "charlie"]) # => [['foo', 0.6875], ['bar', 0.75], ['baz', 0.0]]
