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


sql = "select * from shop "
shops = get_data(sql)
for i in range(len(shops)):
    shop_id = shops[i][0]
    shop_title = shops[i][1]

    sql = "select  sum(to_number(totalSoldQuantity,'9999999999')),insert_date,insert_time from item2 where shop_id = '"+shop_id+"' \
            group by insert_date,insert_time having insert_date in (select min(insert_date) from item2 \
            where shop_id ='"+shop_id+"')"
    rows = get_data(sql)
    total_sold = int(rows[0][0])
    date = rows[0][1]
    time = rows[0][2]
    sql = "select  sum(to_number(totalSoldQuantity,'9999999999')*price) from item2 where shop_id = '"+shop_id+"' group by insert_date having insert_date in (select min(insert_date) \
            from item2 where shop_id='"+shop_id+"')"
    rows = get_data(sql)
    total_sale = int(rows[0][0])

    sql = "insert into daily_info(shop_id,shop_title,total_sold,total_sale,date,time) values(\
            '"+shop_id+"','"+shop_title+"','"+str(total_sold)+"','"+str(total_sale)+"','"+str(date)+"','"+str(time)+"')"
    update_data(sql)


