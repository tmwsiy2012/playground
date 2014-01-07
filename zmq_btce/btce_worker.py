__author__ = 'tmwsiy'
import sys
import time
import zmq
import requests



context = zmq.Context()

# Socket to receive messages on
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:5557")

# Socket to send messages to
sender = context.socket(zmq.PUSH)
sender.connect("tcp://localhost:5558")

# Process tasks forever
while True:
    s = receiver.recv()
    job_params = s.split(',')
    # Simple progress indicator for the viewer
    sys.stdout.write('running...' + s)
    sys.stdout.flush()

    # Do the work
    r =  requests.get('https://btc-e.com/api/2/' + job_params[0] + '/trades')


    # Send results to sink
    sender.send_string('[{"' + job_params[0] + '":"' + job_params[1] + ',' + job_params[2] + '"},' + r.text +']')