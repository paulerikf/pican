from time import sleep

import can
import math

import struct

bus = can.interface.Bus(channel='can0', bustype='socketcan_native')


def send():
    msg = can.Message(arbitration_id=0x4C0,
                      data=8,
                      extended_id=False)
    bus.send(msg)
    sleep(0.001)


def sending():
    while True:
        send()
