#!/usr/bin/env python
# -*- coding:utf-8 -*-
import SocketServer

class Myserver(SocketServer.BaseRequestHandler):

    def handle(self):
        print(self.client_address)  #输出连接的是谁
        conn = self.request
        conn.sendall(bytes('Hello'))
        while True:
            data = conn.recv(1024)
            print(str(data))
            conn.sendall(data)

if __name__ == "__main__":
    server=SocketServer.ThreadingTCPServer(('127.0.0.1',9996),Myserver)
    server.serve_forever()
