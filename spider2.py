#!/usr/bin/python
#coding=utf-8
import psycopg2
import json
from jsonpath import jsonpath
import re
import time
from datetime import datetime
import requests
import logging


#设置编码格式
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#数据库连接
conn = psycopg2.connect(database="postgres", user="postgres", password="123456", host="127.0.0.1", port="5432")
cur = conn.cursor()
#日志配置
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='my.log', level=logging.INFO, format=LOG_FORMAT)
#包头信息
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
cookie = ""
referer = ""

headers = {"User-Agent":user_agent,"Cookie":cookie,'Referer':referer}

#从数据库读取url
sql = "select shop_url from shop "
cur.execute(sql)
rows = cur.fetchall()
shop_name = []
for row in rows:
    shop_name.append(row[0])
count = []
for i in range(len(shop_name)):
    count.append(0)

insert_date = str(datetime.now().date())

for k in range(len(shop_name)):
    url = "https://{}.m.tmall.com/shop/shop_auction_search.do?sort=d&p=1".format(shop_name[k])
    try:
        response = requests.get(url, params=headers)
    except Exception,e:
        print("ERROR in getURL: "+bytes(k))
        print(str(e))
        logging.info(str(e))
    else:
        contents = response.text
        # soup = BeautifulSoup(contents, "html.parser")
        # print(contents)
        unicodestr = json.loads(contents)

        shop_id = jsonpath(unicodestr,"$.shop_id")
        total_pages = jsonpath(unicodestr,"$.total_page")
        total_results = jsonpath(unicodestr,"$.total_results")

        print("************************************************")
        print("No."+bytes(k+1)+"\tshop_id: "+shop_id[0])
        total_page = int(total_pages[0])
        print("total_page: "+str(total_page))
        if total_page > 3:
            total_page = 3
        for i in range(1,total_page+1):
            if i!=1:
                url = "https://{}.m.tmall.com/shop/shop_auction_search.do?sort=d&p={}".format(shop_name[k],i)
                try:
                    response = requests.get(url, params=headers)
                except Exception,e:
                    print("ERROR in : " + bytes(k)+"\tPAGE is : "+bytes(i))
                    print(str(e))
                    logging.info(str(e))
                else:
                    contents = response.text
                # print(contents)
            unicodestr = json.loads(contents)
            item_ids = jsonpath(unicodestr, "$..item_id")#int
            titles = jsonpath(unicodestr, "$..title")
            solds = jsonpath(unicodestr, "$..sold")
            totalSoldQuantitys = jsonpath(unicodestr, "$..totalSoldQuantity")#int
            prices = jsonpath(unicodestr, "$..price")
            print("Page :"+bytes(i))
            for j in range(len(item_ids)):
                print("No."+bytes((i-1)*24+j+1)+"\titem_id: " + bytes(item_ids[j]))
                #print("title: " + titles[j])
                #print("sold: " + solds[j])
                #print("totalSoldQuantity: " + bytes(totalSoldQuantitys[j]))
                #print("price: " + prices[j])

                insert_time = int(time.time())
                #插入数据
                sql = "insert into item2(shop_id,item_id,title,sold,totalSoldQuantity,price,insert_date,insert_time) values " \
                      "('" + shop_id[0] + "','"+str(item_ids[j])+"','"+titles[j].replace("'","`").strip()+"','"+solds[j]+"','"\
                      + str(totalSoldQuantitys[j])+"',"+prices[j]+",'"+insert_date+"','"+str(insert_time)+"')"
                try:
                    cur.execute(sql)
                except Exception,e:
                    cur.execute("rollback")
                    print("ERROR in insert")
                    print(str(e))
                    logging.info(str(e))
                else:
                    cur.execute("commit")
                    count[k] += 1
            time.sleep(2)
        time.sleep(3)
print("----------------------")
for i in range(len(count)):
    print("Total "+bytes(i)+" : "+bytes(count[i]))



