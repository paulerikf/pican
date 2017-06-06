#!/usr/bin/env python

import socket
import struct
from time import time, sleep

import messagebox

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind((TCP_IP, TCP_PORT))
tcp_socket.listen(1)


print('Listening on ', TCP_IP, ':', TCP_PORT, sep='')
conn, addr = tcp_socket.accept()
print('Connection address:', addr)
bus0 = False
now = lambda: int(round(time() * 1000))
time_0 = now()
i = 0

while True:
    recv_msg = messagebox.msg()

    t = now() - time_0
    t_array = [n for n in struct.pack('Q', t)]

    l = 20
    msg = [0] * l

    msg[0] = 0x88
    msg[1] = 0
    msg[2] = 0x00 if bus0 else 0x10
    msg[2] |= recv_msg[1]
    msg[3] = recv_msg[0]

    for i in range(7):
        msg[4 + i] = recv_msg[i + 8]
        msg[12 + i] = t_array[i]

    conn.send(bytearray(msg))

    sleep(0.1)
