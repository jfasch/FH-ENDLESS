#!/usr/bin/env python

import sys
import struct
import socket
import time
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--interface', type=str)
parser.add_argument('--can-id', type=int)
parser.add_argument('--now', type=int, help='timestamp start value (milliseconds)')
parser.add_argument('--interval', type=int, help='interval (milliseconds)')
parser.add_argument('--temperature', type=float, help='temperature (degrees celsius, floating point)')


args = parser.parse_args()

can_iface = args.interface
can_id = args.can_id
now_ms = args.now
interval_ms = args.interval
temperature = args.temperature

FRAME_LAYOUT = "=IB3x8s"
FRAME_SIZE = struct.calcsize(FRAME_LAYOUT)

# cannot mix endiannesses in one single struct, so I have to compose
# the "data" part separately: (timestamp, temperature) as little
# endian uint32
DATA_LAYOUT = "<Ii"
assert struct.calcsize(DATA_LAYOUT) == 8

can_socket = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
can_socket.bind((can_iface,))

while True:
    temperature_milli = int(temperature * 1000)
    data = struct.pack(DATA_LAYOUT, now_ms, temperature_milli)

    print('now_ms', now_ms, 'temperature', temperature)

    frame = struct.pack(FRAME_LAYOUT, can_id, 8, data)
    can_socket.send(frame)

    time.sleep(interval_ms / 1000)
    now_ms += interval_ms
