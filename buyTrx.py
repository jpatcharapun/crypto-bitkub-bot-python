# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 09:35:14 2022

@author: pascharapun.j
"""

from apibutkib import BugKib
import datetime


APIKEYBITKUB='APIKEY_BITKUB'
bitkub = BugKib(_apiKey=APIKEYBITKUB,_apisecret = b'APISECRET_BITKUB')

while True:
    now = datetime.datetime.now().time()
    current_time = now.strftime("%H:%M:%S")
    date = datetime.date(2022,6,9)
    date_of_today = datetime.date.today()
    if date == date_of_today:
        # if now.hour >= 10 and now.minute >= 58 or now.minute:
        # if datetime.datetime.time(12,59) <= datetime.datetime.now():
        if current_time > '12:59:45':
            print("It's 12:59 Time To Buy!")
            a = bitkub.buy('THB_TRX', 5, 2,'LINENOTIFYTOKEN')
            a = bitkub.buy('THB_TRX', 10, 1,'LINENOTIFYTOKEN')
            a = bitkub.buy('THB_TRX', 50, 0.5,'LINENOTIFYTOKEN')
            a = bitkub.buy('THB_TRX', 100, 0.1,'LINENOTIFYTOKEN')
            a = bitkub.buy('THB_TRX', 1000, 0.01,'LINENOTIFYTOKEN')

           
        else:
            print("รอเวลา 12.59 ณ ตอนนี้ เวลา : ",now)
    else:
        print('รอวันที่ 2022-06-09 ณ ตอนนี้ วันที่ :' , date_of_today)
        # a = bitkub.sell('THB_TRX', 54, 5000,'LINENOTIFYTOKEN')
# 5,000
        