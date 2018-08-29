    ##coding=utf-8
    #from pymongo import MongoClient
    #
    #conn = MongoClient('127.0.0.1', 27017)
    #db = conn.testdb  #连接mydb数据库，没有则自动创建
    #collection = db.test_set　　#使用test_set集合，没有则自动创建
    #collection.insert({"name":"zhangsan","age":18})
    #for i in collection.find():
        #print(i)
    #collection.update({"name":"zhangsan"},{'$set':{"age":20}})
#!/usr/bin/python
# -*- coding:utf-8 -*-
from pymongo import MongoClient
conn = MongoClient("mongodb://localhost:27017/")
db = conn.test  #连接mydb数据库，没有则自动创建
my_set = db.student#使用test_set集合，没有则自动创建
my_set.remove({})
my_set.insert({"name":"zhangsan","age":18})
for i in my_set.find():
    print(i)
my_set.update({"name":"zhangsan"},{'$set':{"age":20}})
for i in my_set.find():
    print(i)
