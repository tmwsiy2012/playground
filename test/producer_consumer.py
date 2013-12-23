__author__ = 'tmwsiy'

from threading import Condition, Thread
import time
import random

condition = Condition()

class ConsumerThread(Thread):
    def run(self):
        global queue
        while True:
            condition.acquire()
            if not queue:
                print "Nothing in queue, consumer is waiting"
                condition.wait()
                print "Producer added something to queue and notified the consumer"
            num = queue.pop(0)
            print "Consumed", num
            condition.release()
            time.sleep(random.randint(1,5))

class ProducerThread(Thread):
    def run(self):
        nums = range(5)
        global queue
        while True:
            condition.acquire()
            num = random.choice(nums)
            queue.append(num)
            print "Produced", num
            condition.notify()
            condition.release()
            time.sleep(random.randint(1,5))

queue = []
c1 = ConsumerThread()
p1 = ProducerThread()

c1.start()
p1.start()