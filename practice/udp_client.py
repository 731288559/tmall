#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
ip_port = ('127.0.0.1',9997)

sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0)
while True:
    str_in = str(raw_input('输出: '))
    inp = str(str_in).strip()
    if inp == 'exit':
        break
    sk.sendto(bytes(inp),ip_port)    #UDP每次发送都要指定发送的目标

sk.close()
