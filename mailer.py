#!/usr/bin/env python
# coding: utf-8


import smtplib
from email.mime.text import MIMEText


def send(From, Passwd, Server, Tos, Subject, Txt):
    msg = MIMEText(Txt, _charset='utf8')
    msg['Subject'] = Subject
    msg['From'] = From
    msg['To'] = ','.join(Tos)
    svr = smtplib.SMTP(Server)
    user=From
    svr.ehlo()
    if svr.has_extn('STARTTLS'):
        svr.starttls()
        user=From[:From.index('@')]
    if '' != Passwd > 0:
        svr.login(user, Passwd)
    svr.sendmail(From, Tos, msg.as_string())
    svr.quit()

def test():
    TEXT = u"""
    Hello,
        World~
        你好!
    """
    send('abc@gmail.com', 'passwd', 'smtp.gmail.com:587',
         ["def@163.com"], '[Notice]', TEXT)

