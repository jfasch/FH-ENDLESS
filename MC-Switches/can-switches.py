#!/usr/bin/env python

import sys
import struct
import socket
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--can-interface', type=str, required=True)
parser.add_argument('--can-id', required=True)

args = parser.parse_args()

# CAN parameters
can_iface = args.can_interface
can_id = eval(args.can_id)

class Switch:
    def __init__(self, number):
        self.number = number
        self.state = False
    def set_state(self, state):
        if self.state != state:
            self.state = state
            print(f'{self.number}: {"ON" if self.state else "OFF"}')

switches = [Switch(number) for number in range(4)]

print(f'{len(switches)} switches available:')
for switch in switches:
    print(f'  {switch.number}: {"ON" if switch.state else "OFF"}')

FRAME_LAYOUT = "=IB3x8s"
FRAME_SIZE = struct.calcsize(FRAME_LAYOUT)

DATA_LAYOUT = "????"      # 4 bool values for 4 outputs
assert struct.calcsize(DATA_LAYOUT) == 4

can_socket = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
can_socket.bind((can_iface,))

while True:
    frame = can_socket.recv(FRAME_SIZE)
    frame_can_id, frame_can_dlc, frame_payload = struct.unpack(FRAME_LAYOUT, frame)
    if can_id != frame_can_id:
        continue
    frame_payload = frame_payload[:frame_can_dlc]
    desired_states = struct.unpack(DATA_LAYOUT, frame_payload)
    for switch_number in range(4):
        switches[switch_number].set_state(desired_states[switch_number])
