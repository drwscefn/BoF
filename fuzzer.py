#!/usr/bin/python3

import socket, time, sys

IP = "<IP>"
PORT = <PORT>
timeout = 5

buffer = []
counter = 100
while len(buffer) < 30:
    buffer.append("A" * counter)
    counter += 100

for string in buffer:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        connect = s.connect((IP, PORT))
        s.recv(1024)
        print("Fuzzing with %s bytes" % len(string))
        s.send(string)
        s.recv(1024)
        s.close()
    except:
        print("Could not connect to " + IP + ":" + str(PORT))
        sys.exit(0)
    time.sleep(1)
