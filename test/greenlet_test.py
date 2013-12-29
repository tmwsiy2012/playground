__author__ = 'tmwsiy'

import gevent
from gevent import Greenlet
import time


class MyNoopGreenlet(Greenlet):

    def __init__(self, seconds):
        Greenlet.__init__(self)
        self.seconds = seconds

    def _run(self):
        gevent.sleep(self.seconds)


    def __str__(self):
        return 'MyNoopGreenlet(%s)' % self.seconds

g = MyNoopGreenlet(4)
g.start()
time.sleep(6)
print g.successful()