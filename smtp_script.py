# -*- coding: utf-8 -*-

#发邮件使用的包
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

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

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def send_email():
    today = datetime.datetime.now().date()
    query_date_1 = today + datetime.timedelta(-6)
    query_date_2 = today + datetime.timedelta(0)

    shops = []
    sql = "select shop_id,shop_title from shop"
    shop_info = get_data(sql)
    for j in range(len(shop_info)):
        sql = "select item_id,item_title,item_sold from hot_sell where shop_id='"+shop_info[j][0]+"' and date >= '"+str(query_date_1)+"' and date<= '"+str(query_date_2)+"'"
        rows = get_data(sql)
        new_items = []
        for i in range(len(rows)):
            new_item = {'item_id':rows[i][0],'item_title':rows[i][1],'item_sold':rows[i][2]}
            new_items.append(new_item)
        if new_items != []:
            shop = {'shop_title':shop_info[j][1],'new_items':new_items}
            shops.append(shop)
    shops_today = []
    for j in range(len(shop_info)):
        sql = "select item_id,item_title,item_sold from hot_sell where shop_id='"+shop_info[j][0]+"' and date = '"+str(today)+"' "
        rows = get_data(sql)
        new_items = []
        for i in range(len(rows)):
            new_item = {'item_id':rows[i][0],'item_title':rows[i][1],'item_sold':rows[i][2]}
            new_items.append(new_item)
        if new_items != []:
            shop = {'shop_title':shop_info[j][1],'new_items':new_items}
            shops_today.append(shop)

    content = '<b>今日新增:</b><br>'
    if shops_today == []:
        content += '<b>无</b><br>'
    else:
        content +=\
            "<table border='1' cellspacing='0' cellpadding='3'>\
            <tr>\
                    <th>商店名称</th>\
                    <th>商品编号</th>\
                    <th>商品名称</th>\
                    <th>总销量</th>\
            </tr>"
        for i in shops_today:
            for j in i['new_items']:
                content += "\
                <tr>\
                        <td>"+i['shop_title']+"</td>\
                        <td>"+j['item_id']+"</td>\
                        <td><a  target='_blank' href='https://detail.tmall.com/item.htm?id="+j['item_id']+"'>"+j['item_title']+"</a></td>\
                        <td>"+bytes(j['item_sold'])+"</td>\
                </tr>\
                "
        content +="</table><br>"

    content +="<b>近七天新增:</b><br>"
    if shops == []:
        content += '<b>无</b><br>'
    else:
        content +=\
            "<table border='1' cellspacing='0' cellpadding='3'>\
            <tr>\
                    <th>商店名称</th>\
                    <th>商品编号</th>\
                    <th>商品名称</th>\
                    <th>总销量</th>\
            </tr>"
        for i in shops:
            for j in i['new_items']:
                content += "\
                <tr>\
                        <td>"+i['shop_title']+"</td>\
                        <td>"+j['item_id']+"</td>\
                        <td><a  target='_blank' href='https://detail.tmall.com/item.htm?id="+j['item_id']+"'>"+j['item_title']+"</a></td>\
                        <td>"+bytes(j['item_sold'])+"</td>\
                </tr>\
                "
        content +="</table><br>"
        
            
    html_content="\
    <html>\
            <meta http-equiv='Content-Type' content='text/html; charset=utf-8' />\
            <style>a{text-decoration:none}</style>\
             <head>\
                    <title>热销新品列表</title>\
            </head>\
            <body>\
                    <br>"+content+"\
            </body>\
    </html>"

    #print(html_content)
    from_addr = 'test731test123@163.com'
    password = '123456cjy'
    to_addr = ['zhisong.huang@dotamax.com','hk@dotamax.com']
    smtp_server = 'smtp.163.com'

    msg = MIMEText(html_content, 'html', 'utf-8')

    msg['From'] = from_addr
    msg['To'] = ','.join(to_addr)
    msg['Subject'] = Header(u'热销列表', 'utf-8').encode()
    #print(msg)
    server = smtplib.SMTP(smtp_server, 25)
    #server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()
    print("Done")
