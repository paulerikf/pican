#!/usr/bin/env python

import socket

import struct
from threading import Thread
from time import time

import cangen

TCP_IP = '192.168.42.1'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

can0_socket = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
can0_socket.bind(('can0',))

can1_socket = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
can1_socket.bind(('can1',))

tcp_socket0 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket0.bind((TCP_IP, TCP_PORT))
tcp_socket0.listen(1)


print('Listening on ', TCP_IP, ':', TCP_PORT, sep='')
conn, addr = tcp_socket0.accept()
print('Connection address:', addr)
bus0 = False
now = lambda: int(round(time() * 1000))
time_0 = now()

sender = Thread(target= cangen.sending)
sender.start()

reader0 = Thread(target=send_tcp, args=(can0_socket, conn, time_0))
reader0.start()
reader1 = Thread(target=send_tcp, args=(can1_socket, conn, time_0))
reader1.start()


def send_tcp(can_socket, tcp_socket, start_time):
    while True:
        recv_msg = can_socket.recv(256)

        t = int(round(time() * 1000)) - start_time
        t_array = [n for n in struct.pack('Q', t)]
        # print('msg:', [hex(m) for m in recv_msg])

        l = 20
        msg = [0] * l

        msg[0] = 0x88
        msg[1] = 0
        msg[2] = 0x00 if bus0 else 0x10
        msg[2] |= recv_msg[1]
        msg[3] = recv_msg[0]

        for i in range(8):
            msg[4 + i] = recv_msg[i + 8]
            msg[12 + i] = t_array[i]



        # print('msg:', [hex(m) for m in msg])
        # print(bytearray(msg))
        # print(len(msg))
        tcp_socket.send(bytearray(msg))
