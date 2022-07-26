# -*- coding: utf-8 -*-


# import websocket
import json
import pandas as pd
import pickle
import talib
from datetime import datetime
import numpy
from numpy import mean
import os
import asyncio
import aiofiles
# import websockets
import pprint
import websocket as wb
from apibutkib import BugKib
from pymongo import MongoClient
import datetime
import sys
from termcolor import colored
import numpy as np

bitkub = BugKib(_apiKey='APIKEY_BITKUB' ,_apisecret = b'APISECRET_BITKUB')
excludeProfit = {'LUNA','KUB','DOGE','ZIL','XLM'}
tradeLists = {'GT','BTC','MANA','BNB','ALPHA','SOL','GALA','SUSHI','NEAR','APE','ETH','JFIN','FTM'}
lineOrderToken = 'LINENOTIFYTOKEN'
lineSignalToken = 'LINENOTIFYTOKEN'

bal,data = bitkub.get_balance_assets()
aData = data['result']
# bal = bal['result']
a = {}
b = {}
aOpenOrder ={}
order = {}
bitkub.emergencySell(excludeProfit, lineOrderToken)
listOfBuys = []
def Average(l): 
    avg = sum(l) / len(l) 
    return avg

async def getLastBuyAverage(self,symbol):
    _pair = 'THB_'+symbol
    # bal,aData = self.get_balance_assets()
    # for ba in bal:
    #     if(ba['symbol']=='THB' or ba['symbol']=='DON'):
    #         if(ba['symbol']=='THB'):
    #             pass
    #     else:
    #         symbol = ba['symbol']
    #         amt = ba['available']
    #         
    order[symbol] = bitkub.get_order_history(_pair)
    for ordBuy in order[symbol]:
        if(ordBuy['side']=='buy'):
            print(f"""Side : {ordBuy['side']} ราคา : {ordBuy['rate']}""" )
            listOfBuys.append(float(ordBuy['rate']))
        else:
            break
    average = Average(listOfBuys)
    print(symbol,' Average Buy Price is : ',str(average))

async def getLastBuyAverage(self,symbol):
    listOfBuys = []
    order= {}
    _pair = 'THB_'+symbol
    order[symbol] = bitkub.get_order_history(_pair)
    for ordBuy in order[symbol]:
        if(ordBuy['side']=='buy'):
            print(f"""Side : {ordBuy['side']} ราคา : {ordBuy['rate']}""" )
            listOfBuys.append(round(float(ordBuy['rate']),10))
        else:
            break
    # average = self.Average(listOfBuys)
    average = mean(listOfBuys)
    print('getLastBuyAverage : ' , symbol , ':',average)
    return average

async def doProcessInitialSymbol(self,_objBalanceAsset):
    msg = ''
    for trd in tradeLists:
        aAvailable = _objBalanceAsset[trd]['available']
        aReserved = _objBalanceAsset[trd]['reserved']
        valueNow = aAvailable + aReserved
        if(valueNow == 0):
            _pair = 'THB_'+trd
            aOpenOrder[trd] = bitkub.getSymOpenOrder(_pair)
            aOpenOrderResult = aOpenOrder[trd]['result']
            if(len(aOpenOrderResult)>=1):
                for resultOrder in aOpenOrderResult:
                    _sym=trd
                    _id=resultOrder['id']
                    _sd =resultOrder['side']
                    _hash=resultOrder['hash']
                    _rate=resultOrder['rate']
                    _amount=resultOrder['amount']
                    if(_sd == 'BUY'):
                        bitkub.cancelOpenOrder(_sym, _id, _sd,_hash,_rate,_amount,lineOrderToken)
            print('เริ่ม Init 10 บาท: ', trd)
            bitkub.buyMarket(_pair, 10, 0,lineOrderToken)
            msg += '\nเริ่ม Init 10 บาท: '+ trd
        else:
            msg += '\nไม่ Init : '+ trd
            continue
    return msg


# asyncio.run(getLastBuyAverage(bitkub,'MANA'))
# try:
#     loop = asyncio.get_running_loop() 
# except RuntimeError:
#     loop = None

# if loop and loop.is_running():
#     print('Async event loop already running. Adding coroutine to the event loop.')
    
#     tsk = loop.create_task(doProcessInitialSymbol(bitkub,aData))
#     tsk.add_done_callback(
#         lambda t: print(f'Task done with result={t.result()}'))
# else:
#     print('Starting new event loop')
#     for trd in tradeLists:
#         asyncio.run(getLastBuyAverage(bitkub,trd))
#         asyncio.run(doProcessInitialSymbol(bitkub,aData))
    
# a = bitkub.get_order_history('THB_MANA')