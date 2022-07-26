# # -*- coding: utf-8 -*-


# # import websocket
# import json
# import pandas as pd
# import pickle
# import talib
# from datetime import datetime
# import numpy
# import os
# import asyncio
# import aiofiles
# # import websockets
# import pprint
# import websocket as wb
# from apibutkib import BugKib
# from pymongo import MongoClient
# import datetime
# import sys
# from termcolor import colored
# import numpy as np
# from uuid import uuid4


# # orig_stdout = sys.stdout
# # f = open('C:\Trends.txt', 'a')
# # sys.stdout = f

# # sys.stdout = orig_stdout
# # f.close()


# df = pd.DataFrame()
 
# symbol = 'BTC'
# aUrl = {}
# _timeframe = '5'

# ablaaa = {}
# aOpenOrder= {}
# aOrderHistory = {}
# aDataFrame = {}
# aUrl={}
# APIKEYBITKUB='APIKEY_BITKUB'
# bitkub = BugKib(_apiKey=APIKEYBITKUB,_apisecret = b'APISECRET_BITKUB')
# client = MongoClient('mongodbAddress',27017)
# db = client.TEST
# trend_db = db.trends
# subscribe_db = db.subscribe
# stochrsi_db = db.stochrsis
# macd_db = db.macds
# profitDb = db.profits
# buyDb = db.buys
# sellDb = db.sells
# assetDb = db.assets

# lineOrderToken = 'LINENOTIFYTOKEN'
# lineSignalToken = 'LINENOTIFYTOKEN'

# MyDataFrame ,aUrl[symbol]  = bitkub.get_candle(symbol, timeframe=_timeframe)
# aDataFrame[symbol] = MyDataFrame
# _pair = 'THB_'+str(symbol)
# tb_name = 'TEST_'+ str(datetime.datetime.now().strftime('%Y%m%d'))
# _rat = bitkub.get_last_price(_pair)
# try:
#     # a = bitkub.STOCHRSIsignal(MyDataFrame,symbol)
#     a = bitkub.STOCHRSIsignal(MyDataFrame,symbol)
#     df = pd.DataFrame()
#     table = pd.DataFrame()
#     b = bitkub.MACDsignal(MyDataFrame,symbol)
#     # print(b)
#     aa = stochrsi_db[tb_name].insert_one(a)
#     bb = macd_db[tb_name].insert_one(b)
#     try:
#         a = bitkub.STOCHRSIsignal(MyDataFrame,symbol)
#     except:
#         pass
#     aa = stochrsi_db[tb_name].insert_one(a)
#     try:
#         b = bitkub.MACDsignal(MyDataFrame,symbol)
#     except:
#         pass
   
#     bb = macd_db[tb_name].insert_one(b)
#     text =  symbol + '\n Timeframe : '+ _timeframe +'m \n```' + '\n STOCH RSI : ' + str(a['STOCHRSIk']) + '\n ราคา : ' + str(_rat['last']) + '฿ \n ส่งซิก : ' + a['SignalDesc'] + '```'
#     textMACD = f"\n``` MACD Value : {b['macd_value']} \n MACD HIST Value: {b['macd_hist']} \n MACD Value Signal: {b['value_label']} \n MACD Hist Signal  : {b['signal_label']} \n MACD Signal : {b['signal']} ```"
#     print('\nDoing : ', symbol.strip() , ' RSI Signal : ' , a['signal'] , ' RSI : ' , a['STOCHRSIk'])
#     # amountToSell = (balance_value-2) / _rat['last']
#     # blaaa[symbol] = amountToSell
#     _STOCHRSIk = a['STOCHRSIk']
#     _signal = a['signal']
#     # if(a['signal'] != 'Hold'):
#     bitkub.sendLine(text + textMACD , token = 'LINENOTIFYTOKEN')
    
    
#     # macd_db[APIKEYBITKUB].insert_one(b)
# except:
#     pass



