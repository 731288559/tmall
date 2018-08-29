#coding=utf-8
'''继承式调用'''
import threading
import time
class MyThread(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name = name
    def run(self):
        print("Hello %s"%self.name)
        time.sleep(3)

if __name__ == "__main__":
    t1=MyThread("zhangsan")
    t2=MyThread("lisi")
    t1.start()
    t2.start()

