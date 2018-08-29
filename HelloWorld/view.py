from django.http import HttpResponse
import psycopg2
 
def hello(request):
    conn = psycopg2.connect(database="postgres",user="postgres",password="123456", host="127.0.0.1", port="5432")
    #print "Opened database successfully" 
    sql = "select * from tt"
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()

    return HttpResponse(rows[0])
