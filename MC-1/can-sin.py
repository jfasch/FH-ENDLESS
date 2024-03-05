#!/usr/bin/env python

import sys
import struct
import socket
import time
import argparse
from math import pi, sin


parser = argparse.ArgumentParser()
parser.add_argument('--can-interface', type=str)
parser.add_argument('--can-id', type=int)
parser.add_argument('--start', help='timestamp start value (milliseconds)')
parser.add_argument('--interval', help='interval (milliseconds)')

parser.add_argument('--amplitude', default='1')
parser.add_argument('--hz', type=float, default=1)
parser.add_argument('--phase-shift', default='0')
parser.add_argument('--vertical-shift', type=float, default=0)

args = parser.parse_args()

# CAN parameters
can_iface = args.can_interface
can_id = args.can_id

# sin parameters
start_ms = eval(args.start, {'pi': pi})
interval_ms = eval(args.interval, {'pi': pi})
amplitude = eval(args.amplitude, {'pi': pi})
hz = args.hz
phase_shift = eval(args.phase_shift, {'pi': pi})
vertical_shift = args.vertical_shift

FRAME_LAYOUT = "=IB3x8s"
FRAME_SIZE = struct.calcsize(FRAME_LAYOUT)

# cannot mix endiannesses in one single struct, so I have to compose
# the "data" part separately: (timestamp, temperature) as little
# endian uint32
DATA_LAYOUT = "<Ii"
assert struct.calcsize(DATA_LAYOUT) == 8

can_socket = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
can_socket.bind((can_iface,))

def x_axis(start_ms, interval_ms):
    while True:
        yield start_ms
        time.sleep(interval_ms/1000)
        start_ms += interval_ms
        
def mysin(x, amplitude, hz, phase_shift, vertical_shift):
    return amplitude * sin(hz*(x+phase_shift)) + vertical_shift

for x in x_axis(start_ms, interval_ms):
    y = mysin(x, amplitude=amplitude, hz=hz, phase_shift=phase_shift, vertical_shift=vertical_shift)

    data = struct.pack(DATA_LAYOUT, round(x), round(y))

    print('x', x, 'y', y)

    frame = struct.pack(FRAME_LAYOUT, can_id, 8, data)
    can_socket.send(frame)
