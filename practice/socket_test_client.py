#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
ip_port = ('127.0.0.1',9998)

sk = socket.socket()    #创建socket对象
sk.connect(ip_port) #通过ip和端口连接server端

sk.sendall(bytes('你好'))  #给server端发送信息

server_reply = sk.recv(1024)    #接受消息
print (str(server_reply))    #打印消息

sk.close()  #关闭连接
