#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
ip_port = ('127.0.0.1',9996)
sk = socket.socket()    #创建socket对象
sk.connect(ip_port) #通过ip和端口连接server端
sk.settimeout(5)
while True:
    data = sk.recv(1024)
    print(str(data))
    inp = input('input:')
    sk.sendall(bytes(inp))
    if inp == 'exit':
        break
sk.close()  #关闭连接

