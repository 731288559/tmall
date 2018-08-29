from django.shortcuts import render
import psycopg2
import datetime
import json
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

def get_data(sql):
    conn = psycopg2.connect(database="postgres",user="postgres",password="123456", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.execute(sql)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

def test(request):
    return render(request,'test.html')

def shops(request):
    sql = "select * from shop "
    rows = get_data(sql)
    results = []
    for i in range(len(rows)):
        result = {'shop_id':rows[i][0],'shop_title':rows[i][1],'shop_url':rows[i][2]}
        results.append(result)

    shop_id = request.GET.get('shop_id')
    shop_title = request.GET.get('shop_title')
    if shop_title is None:
        shop_title = results[0]['shop_title']
    if shop_id is None:
        shop_id = results[0]['shop_id']
    sql = "select total_sold,total_sale,time from daily_info where shop_id = '"+shop_id+"' order by date"
    rows = get_data(sql)
    time_all = []
    total_solds = []
    total_sales = []
    for i in rows:
        time_all.append(i[2])
        total_solds.append(i[0])
        total_sales.append(i[1])

    return render(request,'shops.html',{'shop_list':results,'time_all':json.dumps(time_all),
        'total_solds':json.dumps(total_solds),'total_sales':json.dumps(total_sales),'shop_title':shop_title})

def item_list(request):
    shop_title = request.GET.get('shop_title')
    shop_id = request.GET.get('shop_id')
    day_offset = request.GET.get('day_offset')
    today = datetime.datetime.now().date()
    if day_offset is None:
        day_offset = 0
        query_date = today
        print(today)
    else:
        query_date = today + datetime.timedelta(int(day_offset))
        
    sql = "select * from item2 where shop_id='"+shop_id+"' and insert_date='"+str(query_date)+"' order by to_number(sold,'99999') desc"
    rows = get_data(sql)
    results = []
    # print(rows)
    for i in range(len(rows)):
        sql = "select totalSoldQuantity from item2 where item_id='"+rows[i][1]+"' and insert_date='"\
               +str(query_date+datetime.timedelta(int(-1)))+"'"
        y_sold = get_data(sql)
        if y_sold == []:
            y_sold = [(rows[i][4],)]
        change = int(rows[i][4])-int(y_sold[0][0])

        result = {'shop_id':rows[i][0],'item_id':rows[i][1],'title':rows[i][2],
                      'sold':int(rows[i][3]),'totalSoldQuantity':int(rows[i][4]),'price':int(rows[i][5]),
                      'insert_date':rows[i][6],'insert_time':rows[i][7],'y_sold':change,'y_sale':change*rows[i][5]}
        results.append(result)
    sort = request.GET.get('sort')
    sorted_r = []
    if sort is None:
        sorted_r =  sorted(results, key=lambda results: results['y_sold'], reverse=True)
        sort = 'd'
    elif sort == 'm':
         sorted_r =  sorted(results, key=lambda results: results['sold'], reverse=True)
    elif sort == 't':
         sorted_r =  sorted(results, key=lambda results: results['totalSoldQuantity'], reverse=True)
    elif sort == 'p':
         sorted_r =  sorted(results, key=lambda results: results['price'], reverse=True)
    elif sort == 'd':
         sorted_r =  sorted(results, key=lambda results: results['y_sold'], reverse=True)
    else:
         sorted_r =  sorted(results, key=lambda results: results['y_sale'], reverse=True)
    return render(request,'item_list.html',{'item_lists':sorted_r,'day_offset':day_offset,'shop_id':shop_id,'sort':sort,
        'shop_title':shop_title})

def item_detail(request):
    item_id = request.GET.get('item_id')
    sql = "select * from item2 where item_id = '"+item_id+"' order by insert_time desc"
    rows = get_data(sql)
    results = []
    sold_all = []
    time_all = []
    for i in range(len(rows)):
        if i != len(rows)-1:
            change = int(rows[i][4])-int(rows[i+1][4])
        else:
            change = 0
        result = {'shop_id':rows[i][0],'item_id':rows[i][1],'title':rows[i][2],
                      'sold':int(rows[i][3]),'totalSoldQuantity':int(rows[i][4]),'price':int(rows[i][5]),
                      'insert_date':rows[i][6],'insert_time':rows[i][7],'y_sold':change}
        sold_all.append(rows[i][4])
        time_all.append(rows[i][7])
        results.append(result)
    sold_all.reverse()
    time_all.reverse()
    return render(request,'item_detail.html',{'item_detail':results,'sold_all':json.dumps(sold_all),'time_all':json.dumps(time_all)})
def new_hot(request):
    today = datetime.datetime.now().date()
    week_offset = request.GET.get('week_offset')
    if week_offset is None:
        week_offset = 0
    query_date_1 = today + datetime.timedelta((int(week_offset)*7-6))
    query_date_2 = today + datetime.timedelta(int(week_offset)*7)
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
    
    return render(request,'new_hot.html',{'shops':shops,'query_date_1':query_date_1,'query_date_2':query_date_2,'week_offset':week_offset})      
