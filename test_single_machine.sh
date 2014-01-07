#!/bin/bash


python zmq_btce/btce_sink.py &
sleep 1
python zmq_btce/btce_worker.py &
python zmq_btce/btce_worker.py &
sleep 2
python zmq_btce/btce_vent.py &

