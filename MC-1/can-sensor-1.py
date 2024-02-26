#!/usr/bin/env python

import sys
import struct
import socket
import time


can_iface = sys.argv[1]
can_id = int(sys.argv[2])
now_ms = int(sys.argv[3])
interval_ms = int(sys.argv[4])

TEMPERATURE = 42.666

FRAME_LAYOUT = "=IB3x8s"
FRAME_SIZE = struct.calcsize(FRAME_LAYOUT)

# cannot mix endiannesses in one single struct, so I have to compose
# the "data" part separately: (timestamp, temperature) as little
# endian uint32
DATA_LAYOUT = "<2I"
assert struct.calcsize(DATA_LAYOUT) == 8

can_socket = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
can_socket.bind((can_iface,))

while True:
    temperature = int(TEMPERATURE * 1000)
    data = struct.pack(DATA_LAYOUT, now_ms, temperature)

    frame = struct.pack(FRAME_LAYOUT, can_id, 8, data)
    can_socket.send(frame)

    time.sleep(interval_ms / 1000)
    now_ms += interval_ms
