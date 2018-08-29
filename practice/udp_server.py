#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
ip_port = ('127.0.0.1',9997)
sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0)
sk.bind(ip_port)    #绑定ip、端口

while True:
    data = sk.recv(1024)    #recv阻塞，直到接收到客户端传递过来的信息
    print (str(data))
