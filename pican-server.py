#!/usr/bin/env python

import socket

from struct import unpack, pack

from time import time

import array

TCP_IP = '192.168.42.1'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

can_socket = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
can_socket.bind(('vcan0',))

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind((TCP_IP, TCP_PORT))
tcp_socket.listen(1)


print('Listening on ', TCP_IP, ':', TCP_PORT, sep='')
conn, addr = tcp_socket.accept()
print('Connection address:', addr)
bus0 = False
now = lambda: int(round(time() * 1000))
time_0 = now()

while True:
	recv_msg = can_socket.recv(256)

	t = now() - time_0
	t_array = [n for n in pack('Q', t)]
	print('msg:', [hex(m) for m in recv_msg])

	l = 20
	msg = [0] * l

	msg[0] = 0x88
	msg[2] = 0x00 if bus0 else 0x10
	msg[2] |= recv_msg[1]
	msg[3] = recv_msg[0]

	for i in range(8):
		msg[4 + i] = recv_msg[i + 8]
		msg[12 + i] = t_array[i]



	print('msg:', [hex(m) for m in msg])
	# print(bytearray(msg))
	print(len(bytearray(msg)))
	conn.send(bytearray(msg))



