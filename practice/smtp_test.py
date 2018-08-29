# -*- coding: utf-8 -*-

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

from_addr = 'test731test123@163.com'
password = '123456cjy'
to_addr = ['731288559@qq.com','1348509442@qq.com']
smtp_server = 'smtp.163.com'
html_content = '<html><body><h1>Hello</h1>' +'<p>send by</p>' +'</body></html>'
msg = MIMEText(html_content, 'html', 'utf-8')

msg['From'] ='test731test123@163.com' 
msg['To'] = ','.join(to_addr)
msg['Subject'] = Header(u'HHHH', 'utf-8').encode()

print(msg)
server = smtplib.SMTP(smtp_server, 25)
#server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr,to_addr, msg.as_string())
server.quit()
print("Done")

