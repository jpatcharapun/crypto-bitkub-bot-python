# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 10:03:48 2022

@author: prochula
"""

# -*- coding: utf-8 -*-


# import websocket
import json
import pandas as pd
import pickle
import talib
from datetime import datetime
import numpy
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

SOCKET = 'wss://api.bitkub.com/websocket-api/'
#Parameters of the RSI Strategy
pair = {
        'KUB':'market.trade.thb_kub'
        }
RSI_PERIOD = 14
RSI_OVERBOUGHT =70
RSI_OVERSOLD = 30
#Symbol of Ethereum
TRADE_SYMBOL = "ETHUSD"
#Quantity of ETH for a trade
TRADE_QUANTITY = 1
in_position = False
df = pd.DataFrame()
API_KEY = 'xxx'
API_SECRET = 'xxx'
HISTORY_PATH = os.path.join(os.getcwd(), "data_history")
WSS_URL = "wss://api.bitkub.com/websocket-api/"
DATA_STR = ""

coinList = {'ZIL'}
excludeProfit = {'LUNA','KUB','DOGE','ZIL','XLM'}
tradeLists = {'GT','BTC','MANA','BNB','ALPHA','SOL','GALA','SUSHI','NEAR','APE','ETH','JFIN','FTM'}
# tradeOption = {
#                 'GT':{'Buy':50,'Sell':295,'MaxAmt':300,'firstInitial':0,'timeframe':'5','profitTotake':10,'tradeStyle':'fixProfit'},
#                 'MANA':{'Buy':50,'Sell':295,'MaxAmt':300,'firstInitial':0,'timeframe':'5','profitTotake':10,'tradeStyle':'fixProfit'},
#                 'BNB':{'Buy':500,'Sell':594,'MaxAmt':1000,'firstInitial':0,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
#                 'ALPHA':{'Buy':50,'Sell':295,'MaxAmt':300,'firstInitial':0,'timeframe':'5','profitTotake':10,'tradeStyle':'fixProfit'},
#                 'SOL':{'Buy':50,'Sell':195,'MaxAmt':200,'firstInitial':0,'timeframe':'5','profitTotake':10,'tradeStyle':'fixProfit'},
#                 'GALA':{'Buy':50,'Sell':195,'MaxAmt':200,'firstInitial':0,'timeframe':'5','profitTotake':10,'tradeStyle':'fixProfit'},
#                 'SUSHI':{'Buy':50,'Sell':195,'MaxAmt':200,'firstInitial':0,'timeframe':'5','profitTotake':'10','tradeStyle':'fixProfit'},
#                 'BTC':{'Buy':500,'Sell':495,'MaxAmt':1000,'firstInitial':0,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
#             }
tradeOption = { #4099.72
                'DEFAULT':{'Buy':70,'Sell':295,'MaxAmt':280,'firstInitial':0,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
                'GT':{'Buy':70,'Sell':295,'MaxAmt':280,'firstInitial':0,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
                'MANA':{'Buy':70,'Sell':295,'MaxAmt':280,'firstInitial':0,'timeframe':'5','profitTotake':5,'tradeStyle':'stepProfit'},
                'BNB':{'Buy':100,'Sell':594,'MaxAmt':500,'firstInitial':0,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
                'ALPHA':{'Buy':70,'Sell':295,'MaxAmt':280,'firstInitial':0,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
                'SOL':{'Buy':70,'Sell':195,'MaxAmt':280,'firstInitial':0,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
                'GALA':{'Buy':70,'Sell':195,'MaxAmt':280,'firstInitial':0,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
                'SUSHI':{'Buy':70,'Sell':195,'MaxAmt':280,'firstInitial':0,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
                'BTC':{'Buy':100,'Sell':495,'MaxAmt':500,'firstInitial':0,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
                'NEAR':{'Buy':70,'Sell':495,'MaxAmt':280,'firstInitial':0,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
                'APE':{'Buy':70,'Sell':495,'MaxAmt':280,'firstInitial':0,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
                'ETH':{'Buy':70,'Sell':495,'MaxAmt':280,'firstInitial':0,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
                'JFIN':{'Buy':70,'Sell':495,'MaxAmt':280,'firstInitial':0,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
                'FTM':{'Buy':70,'Sell':495,'MaxAmt':280,'firstInitial':0,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
            }
tradeStyleStep = {  # SYMBOL : {'RSI':'PERCENT TO SELL'}
                    'DEFAULT':{
                                 'Range':{'Min':30,'Max':40,'PercentToSell':20},
                                 'Range2':{'Min':40,'Max':50,'PercentToSell':30},
                                 'Range3':{'Min':50,'Max':60,'PercentToSell':40},
                                 'Range4':{'Min':60,'Max':70,'PercentToSell':50},
                                 'Range5':{'Min':70,'Max':80,'PercentToSell':60},
                                 'Range6':{'Min':80,'Max':90,'PercentToSell':80},
                                 'Range7':{'Min':90,'Max':100,'PercentToSell':99}
                        },
                         
                    'BTC':{
                            'Range':{'Min':30,'Max':40,'PercentToSell':20},
                            'Range2':{'Min':40,'Max':50,'PercentToSell':30},
                            'Range3':{'Min':50,'Max':60,'PercentToSell':40},
                            'Range4':{'Min':60,'Max':70,'PercentToSell':50},
                            'Range5':{'Min':70,'Max':80,'PercentToSell':60},
                            'Range6':{'Min':80,'Max':90,'PercentToSell':80},
                            'Range7':{'Min':90,'Max':100,'PercentToSell':99}
                        },
                    
                    'BNB':{
                            'Range':{'Min':30,'Max':40,'PercentToSell':20},
                            'Range2':{'Min':40,'Max':50,'PercentToSell':30},
                            'Range3':{'Min':50,'Max':60,'PercentToSell':40},
                            'Range4':{'Min':60,'Max':70,'PercentToSell':50},
                            'Range5':{'Min':70,'Max':80,'PercentToSell':60},
                            'Range6':{'Min':80,'Max':90,'PercentToSell':80},
                            'Range7':{'Min':90,'Max':100,'PercentToSell':99}
                        },
                    
                    'GT':{
                            'Range':{'Min':30,'Max':40,'PercentToSell':20},
                            'Range2':{'Min':40,'Max':50,'PercentToSell':30},
                            'Range3':{'Min':50,'Max':60,'PercentToSell':40},
                            'Range4':{'Min':60,'Max':70,'PercentToSell':50},
                            'Range5':{'Min':70,'Max':80,'PercentToSell':60},
                            'Range6':{'Min':80,'Max':90,'PercentToSell':80},
                            'Range7':{'Min':90,'Max':100,'PercentToSell':99}
                        },
                    'MANA':{
                            'Range':{'Min':30,'Max':40,'PercentToSell':20},
                            'Range2':{'Min':40,'Max':50,'PercentToSell':30},
                            'Range3':{'Min':50,'Max':60,'PercentToSell':40},
                            'Range4':{'Min':60,'Max':70,'PercentToSell':50},
                            'Range5':{'Min':70,'Max':80,'PercentToSell':60},
                            'Range6':{'Min':80,'Max':90,'PercentToSell':80},
                            'Range7':{'Min':90,'Max':100,'PercentToSell':99}
                        },
                    'ALPHA':{
                            'Range':{'Min':30,'Max':40,'PercentToSell':20},
                            'Range2':{'Min':40,'Max':50,'PercentToSell':30},
                            'Range3':{'Min':50,'Max':60,'PercentToSell':40},
                            'Range4':{'Min':60,'Max':70,'PercentToSell':50},
                            'Range5':{'Min':70,'Max':80,'PercentToSell':60},
                            'Range6':{'Min':80,'Max':90,'PercentToSell':80},
                            'Range7':{'Min':90,'Max':100,'PercentToSell':99}
                        },
                    'SOL':{
                            'Range':{'Min':30,'Max':40,'PercentToSell':20},
                            'Range2':{'Min':40,'Max':50,'PercentToSell':30},
                            'Range3':{'Min':50,'Max':60,'PercentToSell':40},
                            'Range4':{'Min':60,'Max':70,'PercentToSell':50},
                            'Range5':{'Min':70,'Max':80,'PercentToSell':60},
                            'Range6':{'Min':80,'Max':90,'PercentToSell':80},
                            'Range7':{'Min':90,'Max':100,'PercentToSell':99}
                        },
                    'GALA':{
                            'Range':{'Min':30,'Max':40,'PercentToSell':20},
                            'Range2':{'Min':40,'Max':50,'PercentToSell':30},
                            'Range3':{'Min':50,'Max':60,'PercentToSell':40},
                            'Range4':{'Min':60,'Max':70,'PercentToSell':50},
                            'Range5':{'Min':70,'Max':80,'PercentToSell':60},
                            'Range6':{'Min':80,'Max':90,'PercentToSell':80},
                            'Range7':{'Min':90,'Max':100,'PercentToSell':99}
                        },
                    'SUSHI':{
                            'Range':{'Min':30,'Max':40,'PercentToSell':20},
                            'Range2':{'Min':40,'Max':50,'PercentToSell':30},
                            'Range3':{'Min':50,'Max':60,'PercentToSell':40},
                            'Range4':{'Min':60,'Max':70,'PercentToSell':50},
                            'Range5':{'Min':70,'Max':80,'PercentToSell':60},
                            'Range6':{'Min':80,'Max':90,'PercentToSell':80},
                            'Range7':{'Min':90,'Max':100,'PercentToSell':99}
                        },
    }
# 'LUNA':{'Buy':200,'Sell':195,'MaxAmt':200,'firstInitial':194814},
# bitkub = BugKib(_apiKey='APIKEY_BITKUB' ,_apisecret = b'APISECRET_BITKUB')
bitkub = BugKib(_apiKey='APIKEY_BITKUB' ,_apisecret = b'APISECRET_BITKUB')
client = MongoClient('mongodbAddress',27017)
db = client.bitkub
trend_db = db.trends
subscribe_db = db.subscribe
stochrsi_db = db.stochrsis
macd_db = db.macds

lineOrderToken = 'LINENOTIFYTOKEN'
lineSignalToken = 'LINENOTIFYTOKEN'
cash = 0
tb_name = datetime.datetime.now().strftime('%Y%m%d')
ablaaa = {}
aOpenOrder= {}
aOrderHistory = {}
aUrl= {}
Available = {}



def prepare_data_dir():
    print(f"checking history path ({HISTORY_PATH})")
    if not os.path.exists(HISTORY_PATH):
        os.mkdir(HISTORY_PATH)
        print(f"history path is created {HISTORY_PATH}")
        return
    print(f"history path already exists {HISTORY_PATH}")
    
def create_wss_url():
    global WSS_URL
    # symbols = [s for s in list(os.environ.get("CAPTURE_COIN", "").split(","))]
    stream_name = ",".join(
        [f"market.ticker.thb_{s.lower()}" for s in coinList])
    # print(stream_name)
    WSS_URL = f"{WSS_URL}{stream_name}"
    # print(WSS_URL)

async def doProcessInitialSymbol(_objBalanceAsset):
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

##############################################################################################################
async def doProcessMain(ba):
    msg = ba['symbol'] + ':' + str(datetime.datetime.now())
    # lastBuyPrices = {}
    symbol = ba['symbol']
    _pair = 'THB_'+symbol
    _rat = bitkub.get_last_price(_pair)
    # lastBuyPrices[symbol] = lastBuyPrice
    
    # lastPrice = _rat
    Available = ba['available']
    Reserved = ba['reserved']
    
    try:
         balance_value = Available *_rat['last']
    except TypeError:
         pass
     
    amountToSell = float((balance_value-2) / _rat['last'])
    amountToSell = round(amountToSell,8)
    # signal =  []
    _timeframe='5'
    try:
         aAmt = tradeOption[symbol]
         _timeframe = aAmt['timeframe']
    except KeyError:
         aAmt = tradeOption['DEFAULT']
         _timeframe = aAmt['timeframe']
        
    # timeframe = ช่วงเวลาของกราฟที่จะดึงข้อมูล 1, 5, 15, 60, 240, 1D
    MyDataFrame ,aUrl[symbol]  = bitkub.get_candle(symbol, timeframe=_timeframe)
    try:
        a = bitkub.STOCHRSIsignal(MyDataFrame,symbol)
    except:
        pass
    stochrsi_db[tb_name].insert_one(a)
    # b = bitkub.MACDsignal(MyDataFrame,symbol)
    # bb = macd_db[tb_name].insert_one(b)
    
    
    text =  symbol + '\n Timeframe : '+ _timeframe +'m \n```' + '\n RSI : ' + str(a['STOCHRSIk']) + '\n ราคา : ' + str(_rat['last']) + '฿ \n ส่งซิก : ' + a['SignalDesc'] + '```'
    print('\nDoing : ', symbol.strip() , ' RSI Signal : ' , a['signal'] , ' RSI : ' , a['STOCHRSIk'] , str(datetime.datetime.now()))
    lastBuyPrice = bitkub.getLastBuyAverage(symbol)
    _STOCHRSIk = a['STOCHRSIk']
    if(a['signal'] != 'Hold'):
        bitkub.sendLine(text , token = lineSignalToken)
    if symbol in tradeLists:
        # _firstInitial = aAmt['firstInitial']
        aProfitTotake = aAmt['profitTotake']
        _tradeStyle = aAmt['tradeStyle']
        condition = {'cash':cash,'buymai':(balance_value-aAmt['Buy']),'amt/2':(aAmt['Buy']/2),'buy':aAmt['Buy'],'rat':_rat,'sell':amountToSell}
        ablaaa[symbol] = {'Available':Available,'amountToSell':amountToSell,'Reserved':Reserved,'_rat':_rat,'balance_value':balance_value,'Action':condition}
        aOpenOrder[symbol] = bitkub.getSymOpenOrder(_pair)
        aOpenOrderResult = aOpenOrder[symbol]['result']
        # ซื้ออออออออ
        if (a['signal'] == 'Buy'):
            # buyMai = balance_value
            maxBuyAmt = (aAmt['MaxAmt'])
            if(cash >= aAmt['Buy'] and balance_value <= maxBuyAmt):
                if(len(aOpenOrderResult)>=1):
                    for resultOrder in aOpenOrderResult:
                        _sym=symbol
                        _id=resultOrder['id']
                        _sd =resultOrder['side']
                        _hash=resultOrder['hash']
                        _rate=resultOrder['rate']
                        _amount=resultOrder['amount']
                        if(_sd == 'BUY'):
                            bitkub.cancelOpenOrder(_sym, _id, _sd,_hash,_rate,_amount,lineOrderToken)
                print('เงินพอซื้อ : ', symbol)
                msg += 'เงินพอซื้อ : '+ symbol
                if(balance_value <= maxBuyAmt):
                    amtChecked = maxBuyAmt - balance_value
                    amtToBuy = aAmt['Buy']
                    if(amtChecked>=amtToBuy):
                        
                        bitkub.buy(_pair, amtToBuy , _rat['last'],lineOrderToken)
                        print('Buy  : ' , amtToBuy)
                        msg += 'Buy  : ' + str(amtToBuy)
                    else:
                        if(amtChecked>=10):
                            bitkub.buy(_pair, amtChecked , _rat['last'],lineOrderToken)
                            print('Buy : ' , amtChecked)
                            msg += 'Buy : ' + str(amtChecked)
                        else:
                            print('Buy Amount Too Low : ',_pair , ' Amount : ' ,amtChecked)
                            msg += 'Buy Amount Too Low : '+ str(_pair) + ' Amount : ' + str(amtChecked)
                    # bitkub.buy(_pair, aAmt['Buy'], _rat['last'],lineOrderToken)
                        print('สั่งซื้อ : ',_pair)
                        msg += 'สั่งซื้อ : ' + _pair
                else:
                    print('มีแล้วรอขาย : ' , symbol)
                    msg += 'มีแล้วรอขาย : ' + symbol
            else:
                if(balance_value > maxBuyAmt):
                    print('มีเหรียญเยอะกว่าค่าสูงสุดอยู่แล้ว ไม่ซื้อจ๊ะ : ' , symbol)
                    msg += 'มีเหรียญเยอะกว่าค่าสูงสุดอยู่แล้ว ไม่ซื้อจ๊ะ : ' + symbol
                else:
                    if(cash>10):
                        bitkub.buy(_pair, cash , _rat['last'],lineOrderToken)
                        msg += 'ซื้อ ' + _pair + ' ใช้เงิน ' + str(cash) + ' ราคา ' + str(_rat['last'])
                    else:
                        allX = {'Cash':cash,'aAmt[Buy]':aAmt['Buy'] ,'balance_value':balance_value,'maxBuyAmt':maxBuyAmt}
                        print('เงินน้อยไปซื้อไม่ได้ : ' , symbol ,' : ', allX) 
                        msg += 'เงินน้อยไปซื้อไม่ได้ : ' + symbol +' : ', allX
                    # allX = {'Cash':cash,'aAmt[Buy]':aAmt['Buy'] ,'balance_value':balance_value,'maxBuyAmt':maxBuyAmt}
                    # print('เงินน้อยไปซื้อไม่ได้ : ' , symbol ,' : ', allX)
                        bitkub.sendLine(f"เงินคุณไม่พอซื้อ {symbol} โปรดเติมกระสุน \n เงินคุณมี {cash} \n บอทจะซื้อ {aAmt['Buy']}", token=lineOrderToken)
                
             
                # ขายยยยยยยยยยยยยย 
        elif (a['signal'] == 'Sell'):
           
            
            profitMai = balance_value -  (Available*lastBuyPrice)
            # TRADE STYLE
            if(_tradeStyle == 'fixProfit'):
                # FIX RATE
                if(profitMai>=float(aProfitTotake)): 
                    if(Available>=amountToSell and balance_value >= 10):
                        if(len(aOpenOrderResult)>=1):
                            for resultOrder in aOpenOrderResult:
                                _sym=symbol
                                _id=resultOrder['id']
                                _sd =resultOrder['side']
                                _hash=resultOrder['hash']
                                _rate=resultOrder['rate']
                                _amount=resultOrder['amount']
                                if(_sd == 'SELL'):
                                    bitkub.cancelOpenOrder(_sym, _id, _sd,_hash,_rate,_amount,lineOrderToken)
                                    print('ยกเลิกออเดอร์ตั้งขายก่อนหน้า : ',symbol)
                        bitkub.sell(_pair, amountToSell, _rat['last'],lineOrderToken)
                        print('ตั้งขาย : ', _pair , ' Amt:', amountToSell,' Price:', _rat['last'] )
                        bitkub.sendLine('ขายแบบ Fix Rate : ' + symbol + 'STOCH RSI : ' + _STOCHRSIk + ' Sell : '+ amountToSell + '%', ' Price : ' +_rat['last'] + ' LastBuyPrice : ' + lastBuyPrice + ' Profit : '+profitMai , token=lineOrderToken)
                        msg += 'ขายแบบ Fix Rate : ' + symbol + 'STOCH RSI : ' + str(_STOCHRSIk) + ' Sell : '+ str(amountToSell) + '%', ' Price : ' +str(_rat['last']) + ' LastBuyPrice : ' + str(lastBuyPrice) + ' Profit : ' + str(profitMai)
                    else:
                        print('ต้องซื้อก่อนจะขาย : ',symbol)
                        msg += 'ต้องซื้อก่อนจะขาย : '+symbol
                #  IGNORE PROFIT Sell if RSI too High Don't Care Profit
                if(aProfitTotake=='Ignore'): 
                    if(Available>=amountToSell and balance_value >= 10):
                        if(len(aOpenOrderResult)>=1):
                            for resultOrder in aOpenOrderResult:
                                _sym=symbol
                                _id=resultOrder['id']
                                _sd =resultOrder['side']
                                _hash=resultOrder['hash']
                                _rate=resultOrder['rate']
                                _amount=resultOrder['amount']
                                if(_sd == 'SELL'):
                                    bitkub.cancelOpenOrder(_sym, _id, _sd,_hash,_rate,_amount,lineOrderToken)
                                    print('ยกเลิกออเดอร์ตั้งขายก่อนหน้า : ',symbol)
                        bitkub.sell(_pair, amountToSell, _rat['last'],lineOrderToken)
                        print('ตั้งขาย : ', _pair , ' Amt:', amountToSell,' Price:', _rat['last'] )
                        bitkub.sendLine('ขายแบบไม่สนกำไร อิง RSI เป็นหลัก : '+symbol + 'STOCH RSI : ' + _STOCHRSIk + ' Sell : '+ amountToSell + '%'+ ' Price : ' +_rat['last'] + ' LastBuyPrice : ' + lastBuyPrice + ' Profit : '+profitMai , token=lineOrderToken)
                        msg +='ขายแบบไม่สนกำไร อิง RSI เป็นหลัก : '+symbol + 'STOCH RSI : ' + str(_STOCHRSIk) + ' Sell : '+ str(amountToSell) + '%'+ ' Price : ' + str(_rat['last']) + ' LastBuyPrice : ' + str(lastBuyPrice) + ' Profit : '+ str(profitMai)
                    else:
                        msg +='ต้องซื้อก่อนจะขายออก แบบไม่สนใจกำไร : '+symbol
                        print('ต้องซื้อก่อนจะขายออก แบบไม่สนใจกำไร : ',symbol)
        
       
        if(_tradeStyle == 'stepProfit'):
            try:
                 AtradeStep = tradeStyleStep[symbol]
            except KeyError:
                 AtradeStep = tradeStyleStep['DEFAULT']
            
            for _range in AtradeStep:
                _min = AtradeStep[_range]['Min']
                _max = AtradeStep[_range]['Max']
                _PercentToSell = AtradeStep[_range]['PercentToSell']
                # print('_PercentToSell:',_PercentToSell)
                amountToSell = (balance_value*_PercentToSell) / 100 
                # print('amountToSell : (balance_value*_PercentToSell) / 100  : ' ,amountToSell)
                amountToSell = round(amountToSell,15)
                # print('amountToSell : round(amountToSell,10)  : ' ,amountToSell)
                amountToSell = amountToSell / _rat['last']
                # print('amountToSell : amountToSell / _rat["last"] : ' , ('%f' % amountToSell).rstrip('0').rstrip('.'))
                cashRecieve =  amountToSell *  _rat['last']
                a = ('%f' % amountToSell).rstrip('0').rstrip('.')
                # print(a)
                
           
                    
                    
                if(Available>=float(a) and balance_value >= 10 and cashRecieve >= 10 and float(a) >= 0.0001):
                    
                    # DEBUG
                    # if(symbol =='BTC'):
                    #     abtc_STOCHRSIk = _STOCHRSIk
                    #     abtcbalance_value = balance_value
                    #     abtcAvailable = Available
                    #     abtclastBuyPrice = lastBuyPrice
                    #     abtcNowPrice =  _rat['last']
                    #     abtcProfit =  balance_value -  (Available*lastBuyPrice)
                    #     aBtc_min = AtradeStep[_range]['Min']
                    #     aBtc_max = AtradeStep[_range]['Max']
                    #     aBtc_PercentToSell = AtradeStep[_range]['PercentToSell']
                    #     aBtcamountToSell = (balance_value*_PercentToSell) / 100 
                    #     aBtcamountToSell = amountToSell / _rat['last']
                    #     aBtccashRecieve =  amountToSell *  _rat['last']
                    #     aBtca = ('%f' % amountToSell).rstrip('0').rstrip('.')
                    # # END
                    
                    if(_STOCHRSIk >= _min and _STOCHRSIk <= _max):
                        profitMai = balance_value -  (Available*lastBuyPrice)
                        print('Preparing to sell : ',symbol)
                        print('StochRSI : ' , _STOCHRSIk)
                        print('balance_value : ' , balance_value)
                        print('lastBuyPrice : ' , lastBuyPrice)
                        print('CurrentPrice : ' ,  _rat['last'])
                        print('Available : ' , Available)
                        print('profitMai : ' , profitMai)
                        print('aProfitTotake : ' , aProfitTotake)
                        if(profitMai >= float(aProfitTotake)):
                            if(len(aOpenOrderResult)>=1):
                                for resultOrder in aOpenOrderResult:
                                    _sym=symbol
                                    _id=resultOrder['id']
                                    _sd =resultOrder['side']
                                    _hash=resultOrder['hash']
                                    _rate=resultOrder['rate']
                                    _amount=resultOrder['amount']
                                    if(_sd == 'SELL'):
                                        bitkub.cancelOpenOrder(_sym, _id, _sd,_hash,_rate,_amount,lineOrderToken)
                                        print('ยกเลิกออเดอร์ตั้งขายก่อนหน้า : ',symbol)
                            _textSellDescription = '\nขายแบบ STEP ขั้น RSI : '+ str(symbol) + '\nSTOCH RSI : ' + str(_STOCHRSIk) + '\nSell : '+ str(_PercentToSell) + '%' + '\nจำนวน : ' + str(a) + '\nราคาปัจจุบัน : ' + str(_rat['last']) + '\nราคาซื้อล่าสุด : ' + str(lastBuyPrice) + '\nกำไร : '+ str(profitMai)+'฿'
                            bitkub.sell(_pair,  a, _rat['last'],lineOrderToken,_textSellDescription)
                            # print('ขายแบบ STEP ขั้น RSI : ',symbol , ' RSI : ' , _STOCHRSIk , ' Sell : ', _PercentToSell , '%', ' Price : ' ,_rat['last'] , ' LastBuyPrice : ' , lastBuyPrice , ' Profit : ',profitMai)
                            print('ขายแบบ STEP ขั้น RSI : '+ str(symbol) + ' STOCH RSI : ' + str(_STOCHRSIk) + ' Sell : '+ str(_PercentToSell) + '%' + ' จำนวน : ' + str(a) + ' ราคาปัจจุบัน : ' + str(_rat['last']) + ' ซื้อล่าสุดราคา : ' + str(lastBuyPrice) + ' กำไร : '+ str(profitMai))
                            msg += 'ขายแบบ STEP ขั้น RSI : '+ str(symbol) + ' STOCH RSI : ' + str(_STOCHRSIk) + ' Sell : '+ str(_PercentToSell) + '%' + ' จำนวน : ' + str(a) + ' ราคาปัจจุบัน : ' + str(_rat['last']) + ' ซื้อล่าสุดราคา : ' + str(lastBuyPrice) + ' กำไร : '+ str(profitMai)
                            # bitkub.sendLine('ขายแบบ STEP ขั้น RSI : '+ str(symbol) + ' STOCH RSI : ' + str(_STOCHRSIk) + ' Sell : '+ str(_PercentToSell) + '%' + ' จำนวน : ' + str(a) + ' ราคาปัจจุบัน : ' + str(_rat['last']) + ' ซื้อล่าสุดราคา : ' + str(lastBuyPrice) + ' กำไร : '+ str(profitMai) ,token=lineOrderToken)
    print('จบกระบวนการ : ', symbol.strip())
    return msg

#################################################### MAIN ####################################################
                        
if __name__ == "__main__":
    # prepare_data_dir()
    # create_wss_url()
    
    
    # assets = bitkub.get_assets()
    bal,aData = bitkub.get_balance_assets()
    
    
    orig_stdout = sys.stdout
    f = open('C:\BotLogOut.txt', 'a')
    sys.stdout = f
    print('Starting Bot Task :', datetime.datetime.now())
    # for signal in [bitkub.STOCHRSIsignal, bitkub.MACDsignal]:
    #     for stock in [x for x in df.columns if 'stock' in x]: 
    #         df['Close'] = df[stock]
    #         indicator = signal(df)
    #         for sig in indicator.keys():
    #             table.loc[sig, stock] = str(indicator[sig])[:4]
    
    # print(table)
    # for ba in bal:
        ##################################### ซื้อติดเป๋า 
    try:
        loop = asyncio.get_running_loop() 
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        print('Async event loop already running. Adding coroutine to the event loop. doProcessInitialSymbol')
        tsk = loop.create_task(doProcessInitialSymbol(aData['result']))
        tsk.add_done_callback(
            lambda t: print(f'Task done with result={t.result()}'))
    else:
        print('Starting new event loop')
        for trd in tradeLists:
            # asyncio.run(getLastBuyAverage(bitkub,trd))
            asyncio.run(doProcessInitialSymbol(aData['result']))
    # aData = aData['result']
    # for trd in tradeLists:
    #     aAvailable = aData[trd]['available']
    #     aReserved = aData[trd]['reserved']
    #     valueNow = aAvailable + aReserved
    #     if(valueNow == 0):
    #         _pair = 'THB_'+trd
    #         _rat = bitkub.get_last_price(_pair) 
    #         aOpenOrder[trd] = bitkub.getSymOpenOrder(_pair)
    #         aOpenOrderResult = aOpenOrder[trd]['result']
    #         if(len(aOpenOrderResult)>=1):
    #             for resultOrder in aOpenOrderResult:
    #                 _sym=trd
    #                 _id=resultOrder['id']
    #                 _sd =resultOrder['side']
    #                 _hash=resultOrder['hash']
    #                 _rate=resultOrder['rate']
    #                 _amount=resultOrder['amount']
    #                 if(_sd == 'BUY'):
    #                     bitkub.cancelOpenOrder(_sym, _id, _sd,_hash,_rate,_amount,lineOrderToken)
    #         print('เงินพอซื้อ Init 10 บาท: ', trd)
    #         bitkub.buyMarket(_pair, 10, 0,lineOrderToken)
    #     else:
    #         continue
        
        ##################################### ซื้อติดเป๋า 
    for ba in bal:
        
        if(ba['symbol']=='THB' or ba['symbol']=='DON'):
            if(ba['symbol']=='THB'):
                cash = ba['available']
            pass
        else:
            # symbol = ba['symbol']
            try:
                loop = asyncio.get_running_loop() 
            except RuntimeError:
                loop = None

            if loop and loop.is_running():
                print('มีการทำงานใน Loop อยู่แล้ว สร้าง Task รอ Callback doProcessMain : ',ba['symbol'])
                tsk = loop.create_task(doProcessMain(ba))
                tsk.add_done_callback(
                    lambda t: print(f"งานจบด้วยดี doProcessMain result={t.result()} :"))
            else:
                print('ไม่มี Loop ค้าง สั่ง Run doProcessMain :' , ba['symbol'])
                # for trd in tradeLists:
                asyncio.run(doProcessMain(ba))
            # lastBuyPrices = {}
            # symbol = ba['symbol']
            # _pair = 'THB_'+symbol
            # _rat = bitkub.get_last_price(_pair)
            # lastBuyPrice = bitkub.getLastBuyAverage(symbol)
            # lastBuyPrices[symbol] = lastBuyPrice
            
            # lastPrice = _rat
            # Available = ba['available']
            # Reserved = ba['reserved']
            
            # try:
            #      balance_value = Available *_rat['last']
            # except TypeError:
            #      continue
             
            # amountToSell = float((balance_value-2) / _rat['last'])
            # amountToSell = round(amountToSell,8)
            # signal =  []
            # _timeframe='5'
            # try:
            #      aAmt = tradeOption[symbol]
            #      _timeframe = aAmt['timeframe']
            # except KeyError:
            #      aAmt = tradeOption['DEFAULT']
            #      _timeframe = aAmt['timeframe']
                
            # # timeframe = ช่วงเวลาของกราฟที่จะดึงข้อมูล 1, 5, 15, 60, 240, 1D
            # MyDataFrame ,aUrl[symbol]  = bitkub.get_candle(symbol, timeframe=_timeframe)
            # try:
            #     a = bitkub.STOCHRSIsignal(MyDataFrame,symbol)
            # except:
            #     continue
            # aa = stochrsi_db[tb_name].insert_one(a)
            # # b = bitkub.MACDsignal(MyDataFrame,symbol)
            # # bb = macd_db[tb_name].insert_one(b)
            # text =  symbol + '\n Timeframe : '+ _timeframe +'m \n```' + '\n RSI : ' + str(a['STOCHRSIk']) + '\n ราคา : ' + str(_rat['last']) + '฿ \n ส่งซิก : ' + a['SignalDesc'] + '```'
            # print('\nDoing : ', symbol.strip() , ' RSI Signal : ' , a['signal'] , ' RSI : ' , a['STOCHRSIk'])
            # _STOCHRSIk = a['STOCHRSIk']
            # if(a['signal'] != 'Hold'):
            #     bitkub.sendLine(text , token = lineSignalToken)
            # if symbol in tradeLists:
            #     _firstInitial = aAmt['firstInitial']
            #     aProfitTotake = aAmt['profitTotake']
            #     _tradeStyle = aAmt['tradeStyle']
            #     condition = {'cash':cash,'buymai':(balance_value-aAmt['Buy']),'amt/2':(aAmt['Buy']/2),'buy':aAmt['Buy'],'rat':_rat,'sell':amountToSell}
            #     ablaaa[symbol] = {'Available':Available,'amountToSell':amountToSell,'Reserved':Reserved,'_rat':_rat,'balance_value':balance_value,'Action':condition}
            #     aOpenOrder[symbol] = bitkub.getSymOpenOrder(_pair)
            #     aOpenOrderResult = aOpenOrder[symbol]['result']
            #     # ซื้ออออออออ
            #     if (a['signal'] == 'Buy'):
            #         buyMai = balance_value
            #         maxBuyAmt = (aAmt['MaxAmt'])
            #         if(cash >= aAmt['Buy'] and balance_value <= maxBuyAmt):
            #             if(len(aOpenOrderResult)>=1):
            #                 for resultOrder in aOpenOrderResult:
            #                     _sym=symbol
            #                     _id=resultOrder['id']
            #                     _sd =resultOrder['side']
            #                     _hash=resultOrder['hash']
            #                     _rate=resultOrder['rate']
            #                     _amount=resultOrder['amount']
            #                     if(_sd == 'BUY'):
            #                         bitkub.cancelOpenOrder(_sym, _id, _sd,_hash,_rate,_amount,lineOrderToken)
            #             print('เงินพอซื้อ : ', symbol)
                        
            #             if(balance_value <= maxBuyAmt):
            #                 amtChecked = maxBuyAmt - balance_value
            #                 amtToBuy = aAmt['Buy']
            #                 if(amtChecked>=amtToBuy):
                                
            #                     bitkub.buy(_pair, amtToBuy , _rat['last'],lineOrderToken)
            #                     print('Buy  : ' , amtToBuy)
            #                 else:
            #                     if(amtChecked>=10):
            #                         bitkub.buy(_pair, amtChecked , _rat['last'],lineOrderToken)
            #                         print('Buy : ' , amtChecked)
            #                     else:
            #                         print('Buy Amount Too Low : ',_pair , ' Amount : ' ,amtChecked)
            #                 # bitkub.buy(_pair, aAmt['Buy'], _rat['last'],lineOrderToken)
            #                     print('สั่งซื้อ : ',_pair)
            #             else:
            #                 print('มีแล้วรอขาย : ' , symbol)
            #         else:
            #             if(balance_value > maxBuyAmt):
            #                 print('มีเหรียญเยอะกว่าค่าสูงสุดอยู่แล้ว ไม่ซื้อจ๊ะ : ' , symbol)
            #             else:
            #                 if(cash>10):
            #                     bitkub.buy(_pair, cash , _rat['last'],lineOrderToken)
            #                 else:
            #                     allX = {'Cash':cash,'aAmt[Buy]':aAmt['Buy'] ,'balance_value':balance_value,'maxBuyAmt':maxBuyAmt}
            #                     print('เงินน้อยไปซื้อไม่ได้ : ' , symbol ,' : ', allX) 
            #                 # allX = {'Cash':cash,'aAmt[Buy]':aAmt['Buy'] ,'balance_value':balance_value,'maxBuyAmt':maxBuyAmt}
            #                 # print('เงินน้อยไปซื้อไม่ได้ : ' , symbol ,' : ', allX)
            #                     bitkub.sendLine(f"เงินคุณไม่พอซื้อ {symbol} โปรดเติมกระสุน \n เงินคุณมี {cash} \n บอทจะซื้อ {aAmt['Buy']}", token=lineOrderToken)
                        
                     
            #             # ขายยยยยยยยยยยยยย 
            #     elif (a['signal'] == 'Sell'):
                   
                    
            #         profitMai = balance_value -  (Available*lastBuyPrice)
            #         # TRADE STYLE
            #         if(_tradeStyle == 'fixProfit'):
            #             # FIX RATE
            #             if(profitMai>=float(aProfitTotake)): 
            #                 if(Available>=amountToSell and balance_value >= 10):
            #                     if(len(aOpenOrderResult)>=1):
            #                         for resultOrder in aOpenOrderResult:
            #                             _sym=symbol
            #                             _id=resultOrder['id']
            #                             _sd =resultOrder['side']
            #                             _hash=resultOrder['hash']
            #                             _rate=resultOrder['rate']
            #                             _amount=resultOrder['amount']
            #                             if(_sd == 'SELL'):
            #                                 bitkub.cancelOpenOrder(_sym, _id, _sd,_hash,_rate,_amount,lineOrderToken)
            #                                 print('ยกเลิกออเดอร์ตั้งขายก่อนหน้า : ',symbol)
            #                     bitkub.sell(_pair, amountToSell, _rat['last'],lineOrderToken)
            #                     print('ตั้งขาย : ', _pair , ' Amt:', amountToSell,' Price:', _rat['last'] )
            #                     bitkub.sendLine('ขายแบบ Fix Rate : ' + symbol + 'STOCH RSI : ' + _STOCHRSIk + ' Sell : '+ amountToSell + '%', ' Price : ' +_rat['last'] + ' LastBuyPrice : ' + lastBuyPrice + ' Profit : '+profitMai , token=lineOrderToken)
            #                 else:
            #                     print('ต้องซื้อก่อนจะขาย : ',symbol)
            #             #  IGNORE PROFIT Sell if RSI too High Don't Care Profit
            #             if(aProfitTotake=='Ignore'): 
            #                 if(Available>=amountToSell and balance_value >= 10):
            #                     if(len(aOpenOrderResult)>=1):
            #                         for resultOrder in aOpenOrderResult:
            #                             _sym=symbol
            #                             _id=resultOrder['id']
            #                             _sd =resultOrder['side']
            #                             _hash=resultOrder['hash']
            #                             _rate=resultOrder['rate']
            #                             _amount=resultOrder['amount']
            #                             if(_sd == 'SELL'):
            #                                 bitkub.cancelOpenOrder(_sym, _id, _sd,_hash,_rate,_amount,lineOrderToken)
            #                                 print('ยกเลิกออเดอร์ตั้งขายก่อนหน้า : ',symbol)
            #                     bitkub.sell(_pair, amountToSell, _rat['last'],lineOrderToken)
            #                     print('ตั้งขาย : ', _pair , ' Amt:', amountToSell,' Price:', _rat['last'] )
            #                     bitkub.sendLine('ขายแบบไม่สนกำไร อิง RSI เป็นหลัก : '+symbol + 'STOCH RSI : ' + _STOCHRSIk + ' Sell : '+ amountToSell + '%'+ ' Price : ' +_rat['last'] + ' LastBuyPrice : ' + lastBuyPrice + ' Profit : '+profitMai , token=lineOrderToken)
            #                 else:
            #                     print('ต้องซื้อก่อนจะขายออก แบบไม่สนใจกำไร : ',symbol)
                
               
            #     if(_tradeStyle == 'stepProfit'):
            #         try:
            #              AtradeStep = tradeStyleStep[symbol]
            #         except KeyError:
            #              AtradeStep = tradeStyleStep['DEFAULT']
                    
            #         for _range in AtradeStep:
            #             _min = AtradeStep[_range]['Min']
            #             _max = AtradeStep[_range]['Max']
            #             _PercentToSell = AtradeStep[_range]['PercentToSell']
            #             # print('_PercentToSell:',_PercentToSell)
            #             amountToSell = (balance_value*_PercentToSell) / 100 
            #             # print('amountToSell : (balance_value*_PercentToSell) / 100  : ' ,amountToSell)
            #             amountToSell = round(amountToSell,15)
            #             # print('amountToSell : round(amountToSell,10)  : ' ,amountToSell)
            #             amountToSell = amountToSell / _rat['last']
            #             # print('amountToSell : amountToSell / _rat["last"] : ' , ('%f' % amountToSell).rstrip('0').rstrip('.'))
            #             cashRecieve =  amountToSell *  _rat['last']
            #             a = ('%f' % amountToSell).rstrip('0').rstrip('.')
            #             # print(a)
                        
                   
                            
                            
            #             if(Available>=float(a) and balance_value >= 10 and cashRecieve >= 10 and float(a) >= 0.0001):
            #                 print('Preparing to sell')
            #                 # DEBUG
            #                 # if(symbol =='BTC'):
            #                 #     abtc_STOCHRSIk = _STOCHRSIk
            #                 #     abtcbalance_value = balance_value
            #                 #     abtcAvailable = Available
            #                 #     abtclastBuyPrice = lastBuyPrice
            #                 #     abtcNowPrice =  _rat['last']
            #                 #     abtcProfit =  balance_value -  (Available*lastBuyPrice)
            #                 #     aBtc_min = AtradeStep[_range]['Min']
            #                 #     aBtc_max = AtradeStep[_range]['Max']
            #                 #     aBtc_PercentToSell = AtradeStep[_range]['PercentToSell']
            #                 #     aBtcamountToSell = (balance_value*_PercentToSell) / 100 
            #                 #     aBtcamountToSell = amountToSell / _rat['last']
            #                 #     aBtccashRecieve =  amountToSell *  _rat['last']
            #                 #     aBtca = ('%f' % amountToSell).rstrip('0').rstrip('.')
            #                 # # END
                            
            #                 if(_STOCHRSIk >= _min and _STOCHRSIk <= _max):
            #                     print('StochRSI : ' , _STOCHRSIk)
            #                     profitMai = balance_value -  (Available*lastBuyPrice)
            #                     print('balance_value : ' , balance_value)
            #                     print('lastBuyPrice : ' , lastBuyPrice)
                                
            #                     print('Available : ' , Available)
            #                     print('profitMai : ' , profitMai)
            #                     print('aProfitTotake : ' , aProfitTotake)
            #                     if(profitMai >= float(aProfitTotake)):
            #                         if(len(aOpenOrderResult)>=1):
            #                             for resultOrder in aOpenOrderResult:
            #                                 _sym=symbol
            #                                 _id=resultOrder['id']
            #                                 _sd =resultOrder['side']
            #                                 _hash=resultOrder['hash']
            #                                 _rate=resultOrder['rate']
            #                                 _amount=resultOrder['amount']
            #                                 if(_sd == 'SELL'):
            #                                     bitkub.cancelOpenOrder(_sym, _id, _sd,_hash,_rate,_amount,lineOrderToken)
            #                                     print('ยกเลิกออเดอร์ตั้งขายก่อนหน้า : ',symbol)
            #                         _textSellDescription = '\nขายแบบ STEP ขั้น RSI : '+ str(symbol) + '\nSTOCH RSI : ' + str(_STOCHRSIk) + '\nSell : '+ str(_PercentToSell) + '%' + '\nจำนวน : ' + str(a) + '\nราคาปัจจุบัน : ' + str(_rat['last']) + '\nราคาซื้อล่าสุด : ' + str(lastBuyPrice) + '\nกำไร : '+ str(profitMai)+'฿'
            #                         bitkub.sell(_pair,  a, _rat['last'],lineOrderToken,_textSellDescription)
            #                         # print('ขายแบบ STEP ขั้น RSI : ',symbol , ' RSI : ' , _STOCHRSIk , ' Sell : ', _PercentToSell , '%', ' Price : ' ,_rat['last'] , ' LastBuyPrice : ' , lastBuyPrice , ' Profit : ',profitMai)
            #                         print('ขายแบบ STEP ขั้น RSI : '+ str(symbol) + ' STOCH RSI : ' + str(_STOCHRSIk) + ' Sell : '+ str(_PercentToSell) + '%' + ' จำนวน : ' + str(a) + ' ราคาปัจจุบัน : ' + str(_rat['last']) + ' ซื้อล่าสุดราคา : ' + str(lastBuyPrice) + ' กำไร : '+ str(profitMai))
                                    # bitkub.sendLine('ขายแบบ STEP ขั้น RSI : '+ str(symbol) + ' STOCH RSI : ' + str(_STOCHRSIk) + ' Sell : '+ str(_PercentToSell) + '%' + ' จำนวน : ' + str(a) + ' ราคาปัจจุบัน : ' + str(_rat['last']) + ' ซื้อล่าสุดราคา : ' + str(lastBuyPrice) + ' กำไร : '+ str(profitMai) ,token=lineOrderToken)
                    
                # else:
                #     pass
                #     print('Trade Option Not config TradeStyle')
                    
                        
                    
            # text =  '```' + symbol + ' : ' + a['SignalDesc'] + '```'
            # print('Doing : ', symbol , 'RSI Signal : ' , a['signal'] , '| MACD Signal : ',b['signal'])
            # if(a['signal'] != 'Hold'):
                # bitkub.sendLine(text,token = lineSignalToken)
    
    # for s in tradeLists:
        
    #     symbol = s
    #     signal =  []
    #     _pair = 'THB_'+symbol
    #     _amt = tradeAmt[symbol]
    #     if(s=='THB' or s=='DON'):
    #         pass
    #     else:
    #         MyDataFrame = bitkub.get_candle(symbol, timeframe='1')
    #         a = bitkub.STOCHRSIsignal(MyDataFrame,symbol)
    #         aa = stochrsi_db[tb_name].insert_one(a)
    #         # b = bitkub.MACDsignal(MyDataFrame,symbol)
    #         # bb = macd_db[tb_name].insert_one(b)
    #         _rat = bitkub.get_last_price(_pair)
    #         text =  symbol + '\n ```' + '\n RSI : ' + str(a['STOCHRSIk']) + '\n ราคา : ' + str(_rat['last']) + '฿ \n ส่งซิก : *' + a['SignalDesc'] + '*```'
    #         print('Doing : ', symbol , 'RSI Signal : ' , a['signal'] , ' RSI : ' , a['STOCHRSIk'])
    #         if(a['signal'] != 'Hold'):
    #             bitkub.sendLine(text,token = lineSignalToken)
    #             if (a['signal'] == 'Buy'):
    #                 print('ซื้อ ',_pair , )
    #                 _rat = bitkub.get_last_price(_pair)
    #                 bitkub.buy(_pair, _amt['Buy'], _rat['last'],'LINENOTIFYTOKEN')
                    
    #             elif (a['signal'] == 'Sell'):
    #                 MaxAmt
    #                 _rat = bitkub.get_last_price(_pair)
    #                 bitkub.sell(_pair, _amt['Sell'], _rat['last'],'LINENOTIFYTOKEN')
                
                
            # df = pd.DataFrame()
            # a = type(MyDataFrame)
            
            # for i in obj:
               
            # df[f'symbol_{i}'] = pd.Series(i, name = 'close').cumsum()
            
            
            # MyDataSeries = MyDataFrame.squeeze()
            # my_series = MyDataFrame['close'].squeeze()
            # table = pd.DataFrame()
            # MyDataFrame.plot(grid = True)
            
            # b = bitkub.MACDsignal(MyDataFrame)
            # aa = stochrsi_db[tb_name].insert_one(a)
            # macd_db[tb_name].insert_one(b)
            # for signal in [bitkub.STOCHRSIsignal, bitkub.MACDsignal]:
            #     for stock in [x for x in MyDataFrame.columns if 'stock' in x]: 
            #         MyDataFrame['close'] = MyDataFrame[stock]
            #         indicator = signal(MyDataFrame)
            #         for sig in indicator.keys():
            #             table.loc[sig, stock] = str(indicator[sig])[:4]
            # print(table)             
            # closed = obj['close']
            # open = obj['open']
            # high = obj['high']
            # low = obj['low']
            # volume = obj['volume']
            
            
            # signal=STOCHRSIsignal(obj)
            
            # print(f"closed: {closed}")
            # print(f"open: {open}")
            # short_k = talib.STOCHRSI(closed.to_numpy())
            # short_d = talib.STOCHRSI(closed.to_numpy(), timeperiod=14, fastk_period=3, fastd_period=3, fastd_matype=0)
            # long_k = talib.STOCHRSI(closed.to_numpy(), timeperiod=14, fastk_period=3, fastd_period=3, fastd_matype=0)
            # long_d = talib.STOCHRSI(closed.to_numpy(), timeperiod=14, fastk_period=3, fastd_period=3, fastd_matype=0)
                
   
    
    
    
    
    # print(assets)
    # i = 0
    # while i < len(assets):
    #     r = assets[i]
    #     id          = r['id']
    #     info        = r['info']
    #     asset      = r['symbol']
    #     gbal        = r['global']
    #     currency    = r['currency']
        
    #     # print(id,info,asset,gbal,currency)
    #     get_price = bitkub.get_last_price(gbal)
    #     current = 0
    #     if get_price:
    #         current = float(get_price['last'])

    #     # print(f"""Check Assets({colored(asset, 'blue')})\nValue: {colored(f'{current:,}', 'yellow')} per {colored(currency, 'blue')}\n{colored(''.rjust(60, '#'), 'yellow')}""")
    #     obj = bitkub.get_candle(asset, timeframe='1D')
    #     trend = bitkub.trand_ema(asset ,obj, fast_length=7, slow_length=45)
    #     # print(trend)
    #     trend_db[tb_name].insert_one(trend)
        
        
    #     # trend_db[tb_name].insert_one(trend)
        
        
    #     # ถ้า avg < 3 และ trend up
    #     if trend['avg'] < 3 and trend['trend'] == "UP":
    #         subscribe_db[tb_name].insert_one(trend)
        
    #     ### end
    #     print(f"\n{''.rjust(60, '-')}")
    #     i += 1
    # print('start : ',WSS_URL)
    # ws = wb.WebSocketApp(WSS_URL, on_open=on_open, on_close=on_close, on_error=on_error, on_message=on_message)
    # ws.run_forever()
    
    print("จบการทำงาน" , datetime.datetime.now())
    sys.stdout = orig_stdout
    f.close()
#################################################### MAIN ####################################################

# def on_message(ws, message):
#     global closed_prices
#     message = json.loads(message)
#     # print(message)
#     candle = message
#     print(candle['open'])
#     stream = candle['stream']
#     closed = candle['close']
#     open = candle['open']
#     high = candle['highestBid']
#     low = candle['lowestAskl']
#     volume = candle['quoteVolume']
#     last = candle['last']
#     lowestAsk = candle['lowestAsk']
#     lowestAskSize = candle['lowestAskSize']
#     highestBid = candle['highestBid']
#     highestBidSize = candle['highestBidSize']
#     change = candle['change']
#     percentChange = candle['percentChange']
#     baseVolume = candle['baseVolume']
#     quoteVolume = candle['quoteVolume']
#     isFrozen = candle['isFrozen']
#     high24hr = candle['high24hr']
#     low24hr = candle['low24hr']
#     open = candle['open']
#     close = candle['close']
    
#     # "stream": "market.ticker.thb_zil",
#     # "id": 12,
#     # "last": 1.7552,
#     # "lowestAsk": 1.7558,
#     # "lowestAskSize": 556.29657594,
#     # "highestBid": 1.7553,
#     # "highestBidSize": 2301.76038284,
#     # "change": 0.1022,
#     # "percentChange": 6.18,
#     # "baseVolume": 65030601.94591811,
#     # "quoteVolume": 110308290.45,
#     # "isFrozen": 0,
#     # "high24hr": 1.785,
#     # "low24hr": 1.6028,
#     # "open": 1.653,
#     # "close": 1.7552
    
#     is_candle_closed = candle['x']
    
#     if is_candle_closed:
#         closed = candle['c']
#         open = candle['o']
#         high = candle['h']
#         low = candle['l']
#         volume = candle['v']
#         print(f"closed: {closed}")
#         print(f"open: {open}")
#         closed_prices.append(float(closed))

#         if len(closed_prices) > RSI_PERIOD:
#             # closed_prices.pop(0)
#             all_rsi = talib.RSI(np.array(closed_prices), RSI_PERIOD)
#             pprint(f"all_rsi: {all_rsi}")
#             last_rsi = all_rsi[-1]
#             if last_rsi > RSI_OVERBOUGHT:
#                 if in_position:
#                     print("Overbought, sell!")
#                     success = order(SIDE_SELL, TRADE_SIZE, ORDER_TYPE_MARKET, TRADE_SYMBOL)
#                     if success:
#                         in_position = False

#                 else:
#                     print("overbought, but we dont have position")
#             elif last_rsi < RSI_OVERSOLD:
#                 if in_position:
#                     print("oversold but already in position")
#                 else:
#                     print("buy!")
#                     success = order(SIDE_BUY, TRADE_SIZE, ORDER_TYPE_MARKET, TRADE_SYMBOL)
#                     if success:
#                         in_position = True




def get_file_name():
    return os.path.join(HISTORY_PATH, f"{datetime.now().strftime('%Y-%m-%dT%H')}.txt")

def Stoch(close, high, low, smoothk, smoothd, n):
    lowestlow = pd.Series.rolling(low, window=n, center=False).min()
    highesthigh = pd.Series.rolling(high, window=n, center=False).max()
    K = pd.Series.rolling(
        100*((close-lowestlow)/(highesthigh-lowestlow)), window=smoothk).mean()
    D = pd.Series.rolling(K, window=smoothd).mean()
    return K, D

async def parse_socket_data(data):
    global DATA_STR
    lines = f"{DATA_STR}{data}".split("\n")
    print(lines)
    # async with aiofiles.open(get_file_name(), mode="a") as f:
    #     await f.writelines([f"{line}\n" for line in lines])
    #     f.close()
      
# async def collect_bitkub_history():
#     try:
#         async for websocket in websockets.connect(WSS_URL):
#             print('Connecting to websocket')
#             try:
#                 async for message in websocket:
#                     await parse_socket_data(message)
#             except:
#                 print('Websocket reading error')
#     except:
#        print('Cannot connect to websocket')
        
# mystochrsi = Stoch(df.rsi, df.rsi, df.rsi, settings.trade_rsi_k,
#                                settings.trade_rsi_d, settings.trade_rsi_stochastic)

# print(rsi)

def on_open(ws):
    # ws.send("{'event':'addChannel','channel':'ethusdt@kline_1m'}")
    print("connected ")


def on_close(ws):
    print("closed connection")


def on_error(ws, error):
    print(error)




