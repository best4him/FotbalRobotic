#!/usr/bin/python

# Connect a client with a will, then disconnect without DISCONNECT.

import subprocess
import socket
import time

import inspect, os, sys
# From http://stackoverflow.com/questions/279237/python-import-a-module-from-a-folder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"..")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

import mosq_test

rc = 1
keepalive = 60
connect_packet = mosq_test.gen_connect("test-helper", keepalive=keepalive, will_topic="will/qos0/test", will_payload="will-message")
connack_packet = mosq_test.gen_connack(rc=0)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 1888))
sock.send(connect_packet)
connack_recvd = sock.recv(len(connack_packet))

if mosq_test.packet_matches("connack", connack_recvd, connack_packet):
    rc = 0

sock.close()
    
exit(rc)

