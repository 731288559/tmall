#coding=utf-8
import psycopg2
import datetime
import time
import json
import hot_sell_script
import smtp_script

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

def daily_info_script():
    # 今日销量=昨日销量+今日销量差
    sql = "select * from shop "
    shops = get_data(sql)
    for i in range(len(shops)):
        shop_id = shops[i][0]
        shop_title = shops[i][1]
        
        date = datetime.datetime.now().date()
        d_time = int(time.time())
        y_date = date + datetime.timedelta(int(-1))

        sql="select total_sold,total_sale from daily_info where date = '"+str(y_date)+"' and shop_id = '"+shop_id+"'"
        rows = get_data(sql)
        total_sold = int(rows[0][0])
        total_sale = int(rows[0][1])

        sql = "select * from item2 where shop_id ='"+shop_id+"' and insert_date = '"+str(date)+"'"
        rows = get_data(sql)
        y_sold_total = 0
        y_sale_total = 0
        for k in range(len(rows)):
            sql = "select totalSoldQuantity from item2 where item_id='"+rows[k][1]+"' and insert_date='"+str(y_date)+"'"
            y_sold = get_data(sql)
            if y_sold == []:
                y_sold = [(rows[k][4],)]
            change = int(rows[k][4])-int(y_sold[0][0])
            y_sold_total += change
            y_sale_total += change * rows[k][5]
        total_sold += int(y_sold_total)
        total_sale += int(y_sale_total)
        sql = "insert into daily_info(shop_id,total_sold,total_sale,date,time) values('"+shop_id+"','"+str(total_sold)+"','"+str(total_sale)+"','"+str(date)+"','"+str(d_time)+"')"
        print(sql)
        update_data(sql)
if __name__ == "__main__":
    daily_info_script()
    hot_sell_script.hot_sell_script()
    smtp_script.send_email()

