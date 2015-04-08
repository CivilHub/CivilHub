#!/bin/bash

# kill processes that may already run
pkill -9 node
pkill -9 python

# run etherpad-lite server
/bin/bash $HOME/dev/etherpad-lite/bin/run.sh &>/dev/null &

# run Django and python
ipython $HOME/dev/places/manage.py runserver 0.0.0.0:8888

