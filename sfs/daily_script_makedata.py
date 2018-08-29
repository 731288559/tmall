#coding=utf-8
import psycopg2
import datetime
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

# 今日销量=昨日销量+今日销量差
sql = "select * from shop "
shops = get_data(sql)
for i in range(len(shops)):
    shop_id = shops[i][0]
    shop_title = shops[i][1]
    sql = "select insert_date,insert_time from item2 where shop_id='"+shop_id+"' group by insert_date,insert_time order by insert_date"
    times = get_data(sql)
    for j in range(1,len(times)):
        date = times[j][0]
        time = times[j][1]
        sql="select total_sold,total_sale from daily_info where date = '"+str(times[j-1][0])+"' and shop_id = '"+shop_id+"'"
        rows = get_data(sql)
        total_sold = rows[0][0]
        total_sale = rows[0][1]

        sql = "select * from item2 where shop_id ='"+shop_id+"' and insert_date = '"+str(date)+"'"
        rows = get_data(sql)
        y_sold_total = 0
        y_sale_total = 0
        for k in range(len(rows)):
            sql = "select totalSoldQuantity from item2 where item_id='"+rows[k][1]+"' and insert_date='"+str(times[j-1][0])+"'"
            y_sold = get_data(sql)
            if y_sold == []:
                y_sold = [(rows[k][4],)]
            change = int(rows[k][4])-int(y_sold[0][0])
            y_sold_total += change
            y_sale_total += change * rows[k][5]
        total_sold += int(y_sold_total)
        total_sale += int(y_sale_total)
        sql = "insert into daily_info(shop_id,shop_title,total_sold,total_sale,date,time) values(\
                '"+shop_id+"','"+shop_title+"','"+str(total_sold)+"','"+str(total_sale)+"','"+str(date)+"','"+str(time)+"')"
        update_data(sql)
