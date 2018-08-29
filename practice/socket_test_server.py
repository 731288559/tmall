#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
ip_port = ('127.0.0.1',9998)

sk = socket.socket() #创建socket对象
sk.bind(ip_port)    #绑定ip、端口
sk.listen(5)    #监听

while True:
    print ('server waiting...')
    conn,addr = sk.accept() #accept阻塞，直到有连接过来
    client_data = conn.recv(1024)   #recv阻塞，直到接收到客户端传递过来的信息
    print (str(client_data)) #打印
    conn.sendall(bytes('Hello'))    #回发信息

    conn.close()    #关闭连接
