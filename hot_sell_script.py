#coding=utf-8
import psycopg2
import datetime
import time
import json

def get_data(sql):
    conn = psycopg2.connect(database="postgres",user="postgres",password="123456", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.execute(sql)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results
def update_data(sql):
    conn = psycopg2.connect(database="postgres",user="postgres",password="123456", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.execute(sql)
    cur.execute("commit")
    cur.close()
    conn.close()
def hot_sell_script():
    sql = "select * from shop "
    shops = get_data(sql)
    count = 0
    for i in range(len(shops)):
        shop_id = shops[i][0]
        shop_title = shops[i][1]
        sql = "select insert_date,insert_time from item2 where shop_id='"+shop_id+"' group by insert_date,insert_time order by insert_date"
        times = get_data(sql)
        for j in range(len(times)):
            date = times[j][0]
            time = times[j][1]

            sql = "select item_id,title,totalSoldQuantity,insert_date,insert_time from item2 where to_number(sold,'999999')>700 and shop_id='"+shop_id+"' and insert_date='"+str(date)+"' "
            rows = get_data(sql)
            for k in range(len(rows)):
                item_id = rows[k][0]
                item_title = rows[k][1]
                item_sold = rows[k][2]
                date = rows[k][3]
                time = rows[k][4]
                sql = "select * from hot_sell where item_id = '"+item_id+"'"
                hot_goods = get_data(sql)
                if hot_goods == []:
                    sql = "insert into hot_sell(shop_id,item_id,item_title,item_sold,date,time) values('{}','{}','{}','{}','{}',{})".format(\
                            shop_id,item_id,item_title,item_sold,date,time)
                    update_data(sql)
                else:
                    sql = "update hot_sell set item_title='{}' ,item_sold='{}' where item_id='{}'".format(item_title,item_sold,item_id)
                    update_data(sql)
        print("No."+bytes(count)+" shop done.")
        count += 1
if __name__ == "__main__":
    hot_sell_script()
