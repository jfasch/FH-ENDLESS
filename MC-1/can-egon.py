#!/usr/bin/env python

import sys
import struct
import socket
import time
import argparse
from math import pi, sin


parser = argparse.ArgumentParser()
parser.add_argument('--can-interface', type=str, required=True)
parser.add_argument('--can-id', required=True)
parser.add_argument('--interval', help='interval (milliseconds)', type=str, default='1000')

parser.add_argument('--amplitude-temperature', default='1')
parser.add_argument('--hz-temperature', type=float, default=1)
parser.add_argument('--phase-shift-temperature', default='0')
parser.add_argument('--vertical-shift-temperature', type=float, default=0)

parser.add_argument('--amplitude-humidity', default='1')
parser.add_argument('--hz-humidity', type=float, default=1)
parser.add_argument('--phase-shift-humidity', default='0')
parser.add_argument('--vertical-shift-humidity', type=float, default=0)

args = parser.parse_args()

# CAN parameters
can_iface = args.can_interface
can_id = eval(args.can_id)

# sin parameters
interval_ms = eval(args.interval, {'pi': pi})

amplitude_temperature = eval(args.amplitude_temperature, {'pi': pi})
hz_temperature = args.hz_temperature
phase_shift_temperature = eval(args.phase_shift_temperature, {'pi': pi})
vertical_shift_temperature = args.vertical_shift_temperature

amplitude_humidity = eval(args.amplitude_humidity, {'pi': pi})
hz_humidity = args.hz_humidity
phase_shift_humidity = eval(args.phase_shift_humidity, {'pi': pi})
vertical_shift_humidity = args.vertical_shift_humidity

FRAME_LAYOUT = "=IB3x8s"
FRAME_SIZE = struct.calcsize(FRAME_LAYOUT)

# cannot mix endiannesses in one single struct, so I have to compose
# the "data" part separately: (temperature, humidity) as little endian
# (int32, uint32)
DATA_LAYOUT = "<iI"
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


start_ms = int(time.time()*1000)

for x in x_axis(start_ms, interval_ms):
    y_temperature = mysin(x, amplitude=amplitude_temperature, hz=hz_temperature, phase_shift=phase_shift_temperature, vertical_shift=vertical_shift_temperature)
    y_humidity = mysin(x, amplitude=amplitude_humidity, hz=hz_humidity, phase_shift=phase_shift_humidity, vertical_shift=vertical_shift_humidity)

    print('x', x, 'y_temperature', y_temperature, 'y_humidity', y_humidity)

    data = struct.pack(DATA_LAYOUT, int(y_temperature*10), int(y_humidity*10))

    frame = struct.pack(FRAME_LAYOUT, can_id, 8, data)
    can_socket.send(frame)
