# -*- coding: utf-8 -*-

"""
Created on 6/5/16 1:55 PM

@file:abc.py
@author: SPBG Co.,Ltd. ..ing 北京正民惠浩投资管理有限公司 ..ing
"""


from email.mime.text import MIMEText
import smtplib
import logging
logging.basicConfig(level=logging.DEBUG)


msg = MIMEText('hello,send by zhao cheng..', 'plain', 'utf-8')

from_addr = 'zhaocheng@spbgcapital.com'
password = 'tnt78910'
to_addr = '3939789@qq.com'
smtp_server = 'smtp.ym.163.com'

server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
logging.debug('msg %s' % msg.as_string())
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()



