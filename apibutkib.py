# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 09:35:14 2022

@author: pascharapun.j
"""
import hashlib
import hmac
import json
import requests
import sched, time
import pandas as pd
import pandas_ta as ta
import datetime
import os
from uuid import uuid4
from termcolor import colored
import cowsay
import talib
import numpy as np
import asyncio
from numpy import mean
import math
class BugKib:
    API_HOST = 'https://api.bitkub.com'
    

    fund = 500
    gap = 10
    MyWatcher = ['ZIL']

    # API_KEY = apikey
    # API_SECRET = apisecret
    API_BITKUB_HOST='https://api.bitkub.com'
    API_BITKUB_CURRENCY='THB'
    API_BITKUB_TIMEFRAME='30,60,240,1D'
    API_LIMIT=50
    API_EMA_FAST=9
    API_EMA_SLOW=26


    condition = {
                    'THB_ZIL':{'buy':0.55,'sell':25},
                    }

    rebalanceTarget = { 
                        'THB_ZIL':250,
                    }

    errorCode = {
                0:'No error',
                1:'Invalid JSON payload',
                2:'Missing X-BTK-APIKEY',
                3:'Invalid API key',
                4:'API pending for activation',
                5:'IP not allowed',
                6:'Missing / invalid signature',
                7:'Missing timestamp',
                8:'Invalid timestamp',
                9:'Invalid user',
                10:'Invalid parameter',
                11:'Invalid symbol',
                12:'Invalid amount',
                13:'Invalid rate',
                14:'Improper rate',
                15:'Amount too low',
                16:'Failed to get balance',
                17:'Wallet is empty',
                18:'Insufficient balance',
                19:'Failed to insert order into db',
                20:'Failed to deduct balance',
                21:'Invalid order for cancellation',
                22:'Invalid side',
                23:'Failed to update order status',
                24:'Invalid order for lookup',
                25:'KYC level 1 is required to proceed',
                30:'Limit exceeds',
                40:'Pending withdrawal exists',
                41:'Invalid currency for withdrawal',
                42:'Address is not in whitelist',
                43:'Failed to deduct crypto',
                44:'Failed to create withdrawal record',
                45:'Nonce has to be numeric',
                46:'Invalid nonce',
                47:'Withdrawal limit exceeds',
                48:'Invalid bank account',
                49:'Bank limit exceeds',
                50:'Pending withdrawal exists',
                51:'Withdrawal is under maintenance',
                52:'Invalid permission',
                53:'Invalid internal address',
                54:'Address has been deprecated',
                55:'Cancel only mode',
                90:'Server error (please contact support)',
                }
    
    ENDPOINTS = {
    "API_ROOT": "https://api.bitkub.com",
    "STATUS_PATH": "/api/status",
    "SERVERTIME_PATH": "/api/servertime",
    "MARKET_SYMBOLS_PATH": "/api/market/symbols",
    "MARKET_TICKER_PATH": "/api/market/ticker?sym={sym}",
    "MARKET_TRADES_PATH": "/api/market/trades?sym={sym}&lmt={lmt}",
    "MARKET_BIDS_PATH": "/api/market/bids?sym={sym}&lmt={lmt}",
    "MARKET_ASKS_PATH": "/api/market/asks?sym={sym}&lmt={lmt}",
    "MARKET_BOOKS_PATH": "/api/market/books?sym={sym}&lmt={lmt}",
    "MARKET_TRADING_VIEW_PATH": "/tradingview/history?symbol={sym}&resolution={int}&from={frm}&to={to}",
    "MARKET_DEPTH_PATH": "/api/market/depth?sym={sym}&lmt={lmt}",
    "MARKET_WALLET": "/api/market/wallet",
    "MARKET_BALANCES": "/api/market/balances",
    "MARKET_PLACE_BID": "/api/market/place-bid",
    "MARKET_PLACE_BID_TEST": "/api/market/place-bid/test",
    "MARKET_PLACE_ASK": "/api/market/place-ask",
    "MARKET_PLACE_ASK_TEST": "/api/market/place-ask/test",
    "MARKET_PLACE_ASK_BY_FIAT": "/api/market/place-ask-by-fiat",
    "MARKET_CANCEL_ORDER": "/api/market/cancel-order",
    "MARKET_MY_OPEN_ORDERS": "/api/market/my-open-orders",
    "MARKET_MY_ORDER_HISTORY": "/api/market/my-order-history",
    "MARKET_ORDER_INFO": "/api/market/order-info",
    "CRYPTO_ADDRESSES": "/api/crypto/addresses?p={p}&lmt={lmt}",
    "CRYPTO_WITHDRAW": "/api/crypto/withdraw",
    "CRYPTO_INTERNAL_WITHDRAW": "/api/crypto/internal-withdraw",
    "CRYPTO_DEPOSIT_HISTORY": "/api/crypto/deposit-history?p={p}&lmt={lmt}",
    "CRYPTO_WITHDRAW_HISTORY": "/api/crypto/withdraw-history?p={p}&lmt={lmt}",
    "CRYPTO_GENERATE_ADDRESS": "/api/crypto/generate-address?sym={sym}",
    "FIAT_ACCOUNTS": "/api/fiat/accounts?p={p}&lmt={lmt}",
    "FIAT_WITHDRAW": "/api/fiat/withdraw",
    "FIAT_DEPOSIT_HISTORY": "/api/fiat/deposit-history?p={p}&lmt={lmt}",
    "FIAT_WITHDRAW_HISTORY": "/api/fiat/withdraw-history",
    "MARKET_WSTOKEN": "/api/market/wstoken",
    "USER_LIMITS": "/api/user/limits",
    "USER_TRADING_CREDITS": "/api/user/trading-credits",
}
    
    s = sched.scheduler(time.time, time.sleep)
    
    
    def __init__(self,_apiKey='APIKEY_BITKUB' ,_apisecret = b'APISECRET_BITKUB'):
        """
        Library นี้ Copy มาไอวัว
        """
        # apikey = 'APIKEY_BITKUB' 
        # apisecret = b'APISECRET_BITKUB'

        # API info
        self.API_HOST = self.API_HOST
        self.API_KEY = _apiKey
        self.API_SECRET = _apisecret
        self.API_CURRENCY = self.API_BITKUB_CURRENCY
        self.API_TIMEFRAME = self.API_BITKUB_TIMEFRAME
        self.API_LIMIT = int(self.API_LIMIT)
        self.API_EMA_FAST = int(self.API_EMA_FAST)
        self.API_EMA_SLOW = int(self.API_EMA_SLOW)
        self.apiKey = _apiKey
        self.apisecret = _apisecret
        self.API_HEADER = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-BTK-APIKEY': self.API_KEY,
        }
    
    def routeAPI(self, _endpoint, **kwargs):
        """
        Get full endpoint for a specific path.
        """
        return self.API_HOST + self.ENDPOINTS[_endpoint].format(**kwargs)
    
    def json_encode(self,data):
        	return json.dumps(data, separators=(',', ':'), sort_keys=True)
    @staticmethod    
    def __json_encode(data):
        return json.dumps(data, separators=(',', ':'), sort_keys=True)
    
    
    def sign(self,data):
    	j = self.json_encode(data)
    	# print('Signing payload: ' + j)
    	h = hmac.new(self.API_SECRET, msg=j.encode(), digestmod=hashlib.sha256)
    	return h.hexdigest()
    
    def getServerTime(self):
        response = requests.get(self.API_HOST + '/api/servertime')
        ts = int(response.text)
        return(ts)
    
    def timeserver(self):
        response = requests.get(self.API_HOST + '/api/servertime')
        ts = int(response.text)
        return(ts)
    
    def get_wallets_assets(self):
        data = {
            'ts': self.timeserver(),
        }
        signature = self.sign(data)
        data['sig'] = signature

        response = requests.post(self.API_HOST + '/api/market/wallet',
                                 headers=self.API_HEADER, data=self.__json_encode(data))
        obj = json.loads(response.text)
        return(obj)
    
    def get_balance_assets(self):
        data = {
            'ts': self.timeserver(),
        }
        signature = self.sign(data)
        data['sig'] = signature

        response = requests.post(self.API_HOST + '/api/market/balances',
                                 headers=self.API_HEADER, data=self.__json_encode(data))
        obj = json.loads(response.text)
        # print(obj)
        data = [{
            'available': float(obj['result'][self.API_CURRENCY]['available']),
            'reserved': obj['result'][self.API_CURRENCY]['reserved'],
            'symbol': self.API_CURRENCY
        }]
        msg = ""
        if obj['error'] == 0:
            currency = obj['result']
            for i in currency:
                if currency[i]['reserved'] > 0 or currency[i]['available'] > 0 :
                    currency[i]['symbol'] = i
                    data.append(currency[i])
                    msg += f"""
                    Symbol: {currency[i]['symbol']}
                    Available: {obj['result'][currency[i]['symbol']]['available']}
                    Reserved: {obj['result'][currency[i]['symbol']]['reserved']}
                    
                    """
                    
        
        # print(msg)

        return(data,obj)
    
    def get_balance_assets_dict(self):
        data = {
            'ts': self.timeserver(),
        }
        signature = self.sign(data)
        data['sig'] = signature

        response = requests.post(self.API_HOST + '/api/market/balances',
                                 headers=self.API_HEADER, data=self.__json_encode(data))
        obj = json.loads(response.text)
        print(obj)
        data = [{
            'available': float(obj['result'][self.API_CURRENCY]['available']),
            'reserved': obj['result'][self.API_CURRENCY]['reserved'],
            'symbol': self.API_CURRENCY
        }]
        msg = ""
        if obj['error'] == 0:
            currency = obj['result']
            for i in currency:
                if currency[i]['reserved'] > 0 or currency[i]['available'] > 0 :
                    currency[i]['symbol'] = i
                    data.append(currency[i])
                    msg += f"""
                    Symbol: {currency[i]['symbol']}
                    Available: {obj['result'][currency[i]['symbol']]['available']}
                    Reserved: {obj['result'][currency[i]['symbol']]['reserved']}
                    
                    """
                    
        
        # print(msg)

        return(obj,data)
    
    def get_order_history(self,p_sym,_lmt=50,_start=1600756416,_end=9610756416):
        self.getServerTime()
        header = {
    	'Accept': 'application/json',
    	'Content-Type': 'application/json',
    	'X-BTK-APIKEY': self.API_KEY,
        }
        data = {
            'ts': self.getServerTime(),
            'sym':p_sym,
            'lmt':_lmt,
            'start':_start,
            'end':_end 
        }
        signature = self.sign(data)
        data['sig'] = signature
        # print('Payload with signature: ' + json_encode(data))
        response = requests.post(self.API_HOST +  self.ENDPOINTS['MARKET_MY_ORDER_HISTORY'], headers=header, data=self.json_encode(data))
        data = response.json()
        data = data['result']
        # print(response.json())
        
        return(data)
    
    
    
    def get_assets(self):
        response = requests.get(
            self.API_HOST + "/api/market/symbols", headers={}, data={})
        obj = json.loads(response.text)
        if obj['error'] == 0:
            i = 0
            while i < len(obj['result']):
                symbol = str(obj['result'][i]['symbol'])
                obj['result'][i]["global"] = symbol
                obj['result'][i]['symbol'] = symbol[4:]
                obj['result'][i]["currency"] = self.API_CURRENCY
                i += 1
            return obj['result']
        return obj['error']
    
    def get_last_price(self, symbol):
        try:
            rticker = requests.get(
                f'{self.API_HOST}/api/market/ticker?sym={symbol}')
            rticker = rticker.json()
            price = rticker[symbol]
            return price
        except Exception as e:
            print(f"Error: {e}")

        return False
    
    def zero_div(x, y):
        try:
            return x / y
        except ZeroDivisionError:
            return 0

    def Average(self,l):   
        avg = sum(l) / len(l) 
        return avg
    
    def getLastBuyAverage(self,symbol):
        listOfBuys = []
        order= {}
        _pair = 'THB_'+symbol
        order[symbol] = self.get_order_history(_pair)
        for ordBuy in order[symbol]:
            if(ordBuy['side']=='buy'):
                print(f"""Side : {ordBuy['side']} ราคา : {ordBuy['rate']} จำนวน : {ordBuy['amount']}""" )
                listOfBuys.append(round(float(ordBuy['rate']),10))
            else:
                print(f"""Side : {ordBuy['side']} ราคา : {ordBuy['rate']} จำนวน : {ordBuy['amount']}""" )
                break
        # average = self.Average(listOfBuys)
        average = mean(listOfBuys)
        print('getLastBuyAverage : ' , symbol , ':',average)
        return average
        
    def getLastBuyAverageNew(self,symbol):
        a = self.get_order_history('THB_'+symbol,200,1653436800,round(time.time()))
        df = pd.DataFrame(
            a, columns=['side', 'type', 'rate', 'fee', 'credit', 'amount','ts']
            )
        df['ts'] = pd.to_datetime(df['ts'], unit='s')
        df = df.rename({'ts': 'datetime'}, axis=1)
        df = df.sort_values(by="datetime")
        df['Ticker'] = 'NEAR'
        df['amount'] =pd.to_numeric(df['amount'], downcast='float')
        df['rate'] = pd.to_numeric(df['rate'], downcast='float')
        df['THB_InStock']=df['amount']  * df['rate'] 
        df['TotalQty'] = df['amount'].where(df['side'].eq('buy'), -df['amount']).cumsum()
        df['Averaged'] = df.apply(lambda x: ((x.side == "buy") - (x.side == "sell")) * x['THB_InStock'], axis = 1)
        df['TotalQty'] = df['TotalQty'].apply(lambda x: float('%.10f' % x))
        df['Averaged'] = df.groupby('Ticker')['Averaged'].cumsum().div(df['TotalQty'])
        res = df.loc[df.index[-1], "Averaged"]
        return res
    
    def costBasisAveragePrice(self,symbol,timestamp=1653436800,limit=555):
        try:
            a = self.get_order_history('THB_'+symbol,limit,timestamp,round(time.time()))
            df = pd.DataFrame(
                a, columns=['side', 'type', 'rate', 'fee', 'credit', 'amount','ts']
                )

            df['ts'] = pd.to_datetime(df['ts'], unit='s')
            df = df.rename({'ts': 'datetime'}, axis=1)
            df = df.sort_values(by="datetime")
            df['Ticker'] = symbol
            df['amount'] =pd.to_numeric(df['amount'], downcast='float')
            df['rate'] = pd.to_numeric(df['rate'], downcast='float')
            df['fee'] = pd.to_numeric(df['fee'], downcast='float')
            df['credit'] = pd.to_numeric(df['credit'], downcast='float')
            df['THB_InStock']=df['amount']  * df['rate'] 
            df['TotalQty'] = df['amount'].where(df['side'].eq('buy'), -df['amount']).cumsum()
            df['TotalQty'] = df['TotalQty'].apply(lambda x: float('%.10f' % x))
            df1 = (df.copy()[df['side'] == 'buy']
               .assign(CumAmountBuy=df.groupby('Ticker')['THB_InStock'].cumsum())
               .assign(CumQtyBuy=df.groupby('Ticker')['amount'].cumsum()))
            df2 = pd.merge(df,df1,how='left',
                            on=['datetime','side', 'Ticker', 'amount', 'rate', 
                                'THB_InStock', 'TotalQty']).ffill()
            s = df2['CumAmountBuy'] / df2['CumQtyBuy']
            df2['AverageCost'] = np.select([((df2['side'] == 'buy') & (df2['side'].shift() == 'sell')),
                                     (df2['side'] == 'sell')],
                                   [((df2['amount'] * df2['rate'] + df2['TotalQty'].shift() * s.shift()) / df2['TotalQty']),
                                    np.nan],
                                   s)
            df2['AverageCost'] = round(df2['AverageCost'],3).ffill()
            df2 = df2.drop(['CumQtyBuy', 'CumAmountBuy'], axis=1)
            return df2.loc[df2.index[-1], "AverageCost"]
        except IndexError:
            return math.nan
        
    def costBasisAveragePriceWithDF(self,symbol,timestamp=1653436800,limit=555):
        try:
            a = self.get_order_history('THB_'+symbol,limit,timestamp,round(time.time()))
            df = pd.DataFrame(
                a, columns=['side', 'type', 'rate', 'fee', 'credit', 'amount','ts']
                )

            df['ts'] = pd.to_datetime(df['ts'], unit='s')
            df = df.rename({'ts': 'datetime'}, axis=1)
            df = df.sort_values(by="datetime")
            df['Ticker'] = symbol
            df['amount'] =pd.to_numeric(df['amount'], downcast='float')
            df['rate'] = pd.to_numeric(df['rate'], downcast='float')
            df['fee'] = pd.to_numeric(df['fee'], downcast='float')
            df['credit'] = pd.to_numeric(df['credit'], downcast='float')
            df['THB_InStock']=df['amount']  * df['rate'] 
            df['TotalQty'] = df['amount'].where(df['side'].eq('buy'), -df['amount']).cumsum()
            df['TotalQty'] = df['TotalQty'].apply(lambda x: float('%.10f' % x))
            df1 = (df.copy()[df['side'] == 'buy']
               .assign(CumAmountBuy=df.groupby('Ticker')['THB_InStock'].cumsum())
               .assign(CumQtyBuy=df.groupby('Ticker')['amount'].cumsum()))
            df2 = pd.merge(df,df1,how='left',
                            on=['datetime','side', 'Ticker', 'amount', 'rate', 
                                'THB_InStock', 'TotalQty']).ffill()
            s = df2['CumAmountBuy'] / df2['CumQtyBuy']
            df2['AverageCost'] = np.select([((df2['side'] == 'buy') & (df2['side'].shift() == 'sell')),
                                     (df2['side'] == 'sell')],
                                   [((df2['amount'] * df2['rate'] + df2['TotalQty'].shift() * s.shift()) / df2['TotalQty']),
                                    np.nan],
                                   s)
            df2['AverageCost'] = round(df2['AverageCost'],3).ffill()
            df2 = df2.drop(['CumQtyBuy', 'CumAmountBuy'], axis=1)
            return df2.loc[df2.index[-1], "AverageCost"] , df
        except IndexError:
            return math.nan
    
    def getMyMoney(self):
        result = 0
        bal,aData = self.get_balance_assets()
        
        THB = 0
        THBinCOIN = 0
        THBReserve = 0
        for ba in bal:
            if(ba['symbol']=='THB' or ba['symbol']=='DON' or ba['symbol']=='LUNA2'):
                if(ba['symbol']=='THB'):
                    THB = ba['available']
                    THBReserve = ba['reserved']
            else:
                symbol = ba['symbol']
                # amt = ba['available']
                _pair = 'THB_'+symbol
                available = ba['available']
                reserved = ba['reserved']
                try:
                    currentPrice = self.get_last_price(_pair)
                except :
                     currentPrice = 0
                try:
                     # balance_value = amt *currentPrice['last']
                     # result + balance_value
                     myMoney = (reserved + available) * currentPrice['last']
                     THBinCOIN += myMoney
                except TypeError:
                     myMoney = (reserved + available) * currentPrice['last']
                     THBinCOIN += myMoney
                     
        result = (THB+THBinCOIN+THBReserve)
        return result
    
    def checkBalanceAndEmergencySell(self , StopLoss = 8000 , dictExclude = {},_token = ''):
        
        bal,aData = self.get_balance_assets()
        allMoney = self.getMyMoney()
        result = False
        if(float(allMoney)<=float(StopLoss)):
            
            for ba in bal:
                if(ba['symbol']=='THB' or ba['symbol']=='DON' or ba['symbol']=='LUNA2'):
                    if(ba['symbol']=='THB'):
                        pass
                else:
                    symbol = ba['symbol']
                    amt = ba['available']
                    _pair = 'THB_'+symbol
                    if(symbol in dictExclude):
                        continue
                    else:
                        self.sendLine('เริ่มขายราคาตลาด แบบฉุกเฉิน BTC กำลังจะตาย !!!!!',_token)
                        print('checkBalanceAndEmergencySell market : ', _pair, ' ',amt,' ', 0,' ', _token ,'\n')
                        self.sellMarket(_pair, amt, 0, _token ,'')
            result = True
        print('CheckBalanceAndEmergencySell : STOPLOSS at :',StopLoss , ' Now All Money : ' ,allMoney ,' Result :' , result        )
        return result
        
    def emergencySell(self,_dictExclude,_token):
        bal,aData = self.get_balance_assets()
        self.sendLine('เริ่มขายราคาตลาด แบบฉุกเฉิน',_token)
        for ba in bal:
            if(ba['symbol']=='THB' or ba['symbol']=='DON'):
                if(ba['symbol']=='THB'):
                    pass
            else:
                
                symbol = ba['symbol']
                amt = ba['available']
                _pair = 'THB_'+symbol
                if(symbol in _dictExclude):
                    continue
                else:
                    self.sellMarket(_pair, amt, 0, _token ,'')
    
    def buy(self,_pair,_amt,_rat,_token,_txtOptional=''):
        header = {
    	'Accept': 'application/json',
    	'Content-Type': 'application/json',
    	'X-BTK-APIKEY': self.API_KEY,
        }
        data = {
            'sym': _pair,
            'amt': _amt, # THB amount you want to spend
            'rat': _rat,
            'typ': 'limit',
            'ts': self.getServerTime(),
        }
        signature = self.sign(data)
        data['sig'] = signature
        
        # print('Payload with signature: ' + self.json_encode(data))
        response = requests.post(self.API_HOST + '/api/market/place-bid', headers=header, data=self.json_encode(data))
        res = response.json()
        if(res['error']==0):
            self.sendLine('ซื้อ Order :{} \n ที่ราคา : {:,.3f} \n จ่ายไป : {}฿ \n ได้มา : {} \n โดนค่า Fee {:,.3f}฿ \n ใช้ Credit Fee {}฿ {}'.format(_pair,_rat,_amt,res['result']['rec'],res['result']['fee'],res['result']['cre'],_txtOptional),token=_token)
        else:
            self.sendLine('ซื้อ Error :{} ที่ราคา : {:,.3f} จำนวน : {} ผลลัพธ์ {} {}'.format(_pair,_rat,_amt,self.errorCode[res['error']],_txtOptional),token=_token)
        obj = json.loads(response.text)
        return obj
    
    async def buyAsync(self,_pair,_amt,_rat,_token,_txtOptional=''):
        header = {
    	'Accept': 'application/json',
    	'Content-Type': 'application/json',
    	'X-BTK-APIKEY': self.API_KEY,
        }
        data = {
            'sym': _pair,
            'amt': _amt, # THB amount you want to spend
            'rat': _rat,
            'typ': 'limit',
            'ts': self.getServerTime(),
        }
        signature = self.sign(data)
        data['sig'] = signature
        res = True
        # print('Payload with signature: ' + self.json_encode(data))
        response = requests.post(self.API_HOST + '/api/market/place-bid', headers=header, data=self.json_encode(data))
        res = response.json()
        if(res['error']==0):
            self.sendLine('ซื้อ Order :{} \n ที่ราคา : {:,.3f} \n จ่ายไป : {}฿ \n ได้มา : {} \n โดนค่า Fee {:,.3f}฿ \n ใช้ Credit Fee {}฿ {}'.format(_pair,_rat,_amt,res['result']['rec'],res['result']['fee'],res['result']['cre'],_txtOptional),token=_token)
        else:
            self.sendLine('ซื้อ Error :{} ที่ราคา : {:,.3f} จำนวน : {} ผลลัพธ์ {} {}'.format(_pair,_rat,_amt,self.errorCode[res['error']],_txtOptional),token=_token)
            res = False
        obj = json.loads(response.text)
        return obj , res
    
    def buyMarket(self,_pair,_amt,_rat,_token,_txtOptional=''):
        header = {
    	'Accept': 'application/json',
    	'Content-Type': 'application/json',
    	'X-BTK-APIKEY': self.API_KEY,
        }
        data = {
            'sym': _pair,
            'amt': _amt, # THB amount you want to spend
            'rat': 0,
            'typ': 'market',
            'ts': self.getServerTime(),
        }
        signature = self.sign(data)
        data['sig'] = signature
        
        # print('Payload with signature: ' + self.json_encode(data))
        response = requests.post(self.API_HOST + '/api/market/place-bid', headers=header, data=self.json_encode(data))
        res = response.json()
        if(res['error']==0):
            self.sendLine('ซื้อ Order :{} \n ที่ราคา : {:,.3f} \n จ่ายไป : {}฿ \n ได้มา : {} \n โดนค่า Fee {:,.3f}฿ \n ใช้ Credit Fee {}฿ {}'.format(_pair,_rat,_amt,res['result']['rec'],res['result']['fee'],res['result']['cre'],_txtOptional),token=_token)
        else:
            self.sendLine('ซื้อ Error :{} ที่ราคา : {:,.3f} จำนวน : {} ผลลัพธ์ {} {}'.format(_pair,_rat,_amt,self.errorCode[res['error']],_txtOptional),token=_token)
        obj = json.loads(response.text)
        return obj
    
    def sell(self,_pair,_amt,_rat,_token ,_txtOptional=''):
        header = {
    	'Accept': 'application/json',
    	'Content-Type': 'application/json',
    	'X-BTK-APIKEY': self.API_KEY,
        }
        data = {
            'sym': _pair,
            'amt': _amt, # amount you want to spend
            'rat': _rat,
            'typ': 'limit',
            'ts': self.getServerTime(),
        }
        signature = self.sign(data)
        data['sig'] = signature
    
        # print('Payload with signature: ' + self.json_encode(data))
    
        response = requests.post(self.API_HOST + '/api/market/place-ask', headers=header, data=self.json_encode(data))
        res = response.json()
        #data = data['result']
        if(res['error']==0):
            self.sendLine('ขาย Order :{} \n ที่ราคา : {:,.3f} \n จำนวน : {} \n ได้เงิน : {} \n โดนค่า Fee {:,.3f}฿ \n ใช้ Credit Fee {}฿ {}'.format(_pair,_rat,_amt,res['result']['rec'],res['result']['fee'],res['result']['cre'],_txtOptional),token=_token)
        else:
           
            self.sendLine('ขาย Error :{} ที่ราคา : {:,.3f} จำนวน : {} ผลลัพธ์ {} {}'.format(_pair,_rat,_amt,self.errorCode[res['error']],_txtOptional),token=_token)
    
        obj = json.loads(response.text)
        return obj
    
    async def sellAsync(self,_pair,_amt,_rat,_token ,_txtOptional=''):
        header = {
    	'Accept': 'application/json',
    	'Content-Type': 'application/json',
    	'X-BTK-APIKEY': self.API_KEY,
        }
        data = {
            'sym': _pair,
            'amt': _amt, # amount you want to spend
            'rat': _rat,
            'typ': 'limit',
            'ts': self.getServerTime(),
        }
        signature = self.sign(data)
        data['sig'] = signature
    
        # print('Payload with signature: ' + self.json_encode(data))
    
        response = requests.post(self.API_HOST + '/api/market/place-ask', headers=header, data=self.json_encode(data))
        res = response.json()
        #data = data['result']
        if(res['error']==0):
            self.sendLine('ขาย Order :{} \n ที่ราคา : {:,.3f} \n จำนวน : {} \n ได้เงิน : {} \n โดนค่า Fee {:,.3f}฿ \n ใช้ Credit Fee {}฿ {}'.format(_pair,_rat,_amt,res['result']['rec'],res['result']['fee'],res['result']['cre'],_txtOptional),token=_token)
        else:
           
            self.sendLine('ขาย Error :{} ที่ราคา : {:,.3f} จำนวน : {} ผลลัพธ์ {} {}'.format(_pair,_rat,_amt,self.errorCode[res['error']],_txtOptional),token=_token)
    
        obj = json.loads(response.text)
        return obj
    
    def getBankAccount(self):
        header = {
    	'Accept': 'application/json',
    	'Content-Type': 'application/json',
    	'X-BTK-APIKEY': self.API_KEY,
        }
        data = {
            'ts': self.getServerTime()
        }
        signature = self.sign(data)
        data['sig'] = signature
    
        # print('Payload with signature: ' + self.json_encode(data))
    
        response = requests.post(self.API_HOST + '/api/fiat/accounts', headers=header, data=self.json_encode(data))
        res = response.json()
        #data = data['result']
       
        return res
    
    def withdrawFiat(self,_bankAccount,_Amount,_token):
        header = {
    	'Accept': 'application/json',
    	'Content-Type': 'application/json',
    	'X-BTK-APIKEY': self.API_KEY,
        }
        data = {
            'id': _bankAccount,
            'amt': _Amount ,# amount 
            'ts': self.getServerTime(),
        }
        signature = self.sign(data)
        data['sig'] = signature
        response = requests.post(self.API_HOST + '/api/fiat/withdraw', headers=header, data=self.json_encode(data))
        res = response.json()
        #data = data['result']
        if(res['error']==0):
            self.sendLine('ถอนเงินไปที่ : ' + str(_bankAccount) + ' จำนวน : ' +str(_Amount),token=_token)
        else:
            self.sendLine('ถอนเงิน Error : {} '.format(self.errorCode[res['error']]),token=_token)
        print('fiat Withdrawal : ' + str(res))
        return res
        
    
    def sellMarket(self,_pair,_amt,_rat,_token ,_txtOptional=''):
        header = {
    	'Accept': 'application/json',
    	'Content-Type': 'application/json',
    	'X-BTK-APIKEY': self.API_KEY,
        }
        data = {
            'sym': _pair,
            'amt': _amt, # amount you want to spend
            'rat': 0,
            'typ': 'market',
            'ts': self.getServerTime(),
        }
        signature = self.sign(data)
        data['sig'] = signature
    
        # print('Payload with signature: ' + self.json_encode(data))
    
        response = requests.post(self.API_HOST + '/api/market/place-ask', headers=header, data=self.json_encode(data))
        res = response.json()
        #data = data['result']
        if(res['error']==0):
            self.sendLine('ขายราคาตลาดสด :{} \n ที่ราคา : {:,.3f} \n จำนวน : {} \n ได้เงิน : {} \n โดนค่า Fee {:,.3f}฿ \n ใช้ Credit Fee {}฿ {}'.format(_pair,_rat,_amt,res['result']['rec'],res['result']['fee'],res['result']['cre'],_txtOptional),token=_token)
        else:
           
            self.sendLine('ขายราคาตลาดสด Error :{} ที่ราคา : {:,.3f} จำนวน : {} ผลลัพธ์ {} {}'.format(_pair,_rat,_amt,self.errorCode[res['error']],_txtOptional),token=_token)
    
        return response
    
    def CheckCondition(self,sc,coin,price):
        # coin= 'THB_BTC', price = 1050000
        text = ''
        check_buy = self.condition[coin]['buy']
        if price <= check_buy:
            txt = '{} ราคาลงแล้ว เหลือ: {:,.3f} รีบซื้อด่วน!\n(ราคาที่อยากได้: {:,.3f})'.format(coin,price,check_buy)
            #print(txt)
            text += txt + '\n'
            self.sendLine(text)
            
        check_sell = self.condition[coin]['sell']
        if price >= check_sell:
            txt = '{} ราคาขึ้นแล้ว ล่าสุดเป็น: {:,.3f} รีบขายด่วน!\n(ราคาที่อยากขาย: {:,.3f})'.format(coin,price,check_sell)
            #print(txt)
            text += txt + '\n'
            self.sendLine(text)
        # print('CheckCondition',coin,price)
        # s.enter(10, 1, CheckCondition, kwargs={'sc':s,'coin': coin,'price': price})
        return text
    
    
    def checkBalance(self):
        header = {
    	'Accept': 'application/json',
    	'Content-Type': 'application/json',
    	'X-BTK-APIKEY': self.API_KEY,
        }
        data = {
            'ts': self.getServerTime(),
        }
        signature = self.sign(data)
        data['sig'] = signature
        # print('Payload with signature: ' + json_encode(data))
        response = requests.post(self.API_HOST + '/api/market/balances', headers=header, data=self.json_encode(data))
        data = response.json()
        data = data['result']
        # print(response.json())
        
        return(data)
    
    def getSymOpenOrder(self,_sym ):
        header = {
    	'Accept': 'application/json',
    	'Content-Type': 'application/json',
    	'X-BTK-APIKEY': self.API_KEY,
        }
        data = {
            'ts': self.getServerTime(),
            'sym':_sym,
        }
        signature = self.sign(data)
        data['sig'] = signature
        # print('Payload with signature: ' + json_encode(data))
        response = requests.post(self.API_HOST + '/api/market/my-open-orders', headers=header, data=self.json_encode(data))
        data = response.json()
        # data = data['result']
        # print(response.json())
        
        return(data)
    
    def cancelOpenOrder(self,_sym,_id ,_sd ,_hash,_rate,_amount, _token ):
        header = {
    	'Accept': 'application/json',
    	'Content-Type': 'application/json',
    	'X-BTK-APIKEY': self.API_KEY,
        }
        data = {
            'ts': self.getServerTime(),
            'sym':_sym,
            'id':_id,
            'sd':_sd,
            'hash':_hash,
        }
        signature = self.sign(data)
        data['sig'] = signature
        # print('Payload with signature: ' + json_encode(data))
        response = requests.post(self.API_HOST + '/api/market/cancel-order', headers=header, data=self.json_encode(data))
        data = response.json()
        # print('order Cancel',data)
        # data = data['result']
        # print(response.json())
        if(data['error']==0):
            self.sendLine('Cancel Order SYM:{} \n SIDE:{} \n RATE:{} \n AMOUNT:{}'.format(_sym,_sd,_rate,_amount),token=_token)
        else:
           
            self.sendLine('Cancel Order Error {} , {} , {} '.format(_sym,_id,_sd,self.errorCode[data['error']]),token=_token)
        return(data)
        
    
    def sendLine(self,_msg,token= 'LINENOTIFYTOKEN'):
        url = "https://notify-api.line.me/api/notify"
        headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
        r = requests.post(url, headers=headers, data = {'message':_msg})
        # print (r.text)
        
    def getAllPrice(self):
        response = requests.get(self.API_HOST + '/api/market/ticker')
        result = response.json()
        return result
        
    def calc(self):
        
        allText = ''
        for c in self.MyWatcher:
            sym = c
            pairedSym = 'THB_'+sym
            rebalText = self.rebalance(pairedSym , sym , self.rebalanceTarget[pairedSym] , False ,self.gap)
                             
            result = self.getAllPrice()
            dataBalance = self.checkBalance()
            
            THB = dataBalance['THB']['available']
            THBReserve = dataBalance['THB']['reserved']
            THBinCOIN = 0
            
            data = result['THB_'+sym]
            last = data['last']
            available = dataBalance[c]['available']
            reserved = dataBalance[c]['reserved']
            myMoney = (reserved + available) * last
            xx = THBinCOIN + myMoney
            THBinCOIN = xx
            # print(sym, last)
            # rebalText = rebalance('THB_'+sym,sym,rebalanceTarget['THB_'+sym],True)
            text = ' {} : {}\n Has : {}{} \n Order : {} {}\n THB : {:,.2f}฿ \n {} \n'.format(str(sym),str(last),str(available),str(sym),str(reserved),str(sym),myMoney,rebalText)
            allText += text
        if(THBReserve==0):
            x =(THB + THBinCOIN) - self.fund
        else:
            x = (THBReserve +(THB + THBinCOIN)) - self.fund 
        xText = '{:,.2f}฿'.format(x)
        sendBalanceText =' ทุน : {}฿ \n {} : {}฿  \n เงินในเหรียญ : {:,.2f}฿ \n เงินใน Order : {:,.2f}฿ \n กำไรขาดทุน  {:,.2f}฿ \n '.format(str(self.fund),str('เงินสด'),str(THB),THBinCOIN,THBReserve,x) 
        self.sendLine( '```'+allText+'```' + '\n ' +  '```' + sendBalanceText + '```',token=_token)    
        
        # sc.enter(60, 1, calc, (sc,))
    def balances(self):
        header = {
    	'Accept': 'application/json',
    	'Content-Type': 'application/json',
    	'X-BTK-APIKEY': self.API_KEY,
        }
        data = {
            'ts': self.getServerTime(),
        }
        signature = self.sign(data)
        data['sig'] = signature
        # print('Payload with signature: ' + json_encode(data))
        response = requests.post(self.API_HOST + '/api/market/balances', headers=header, data=self.json_encode(data))
        data = response.json()
        #data = data['result']
        # print(response.json())
        return(data)
    
    
    def ticker(self,_sym):
        # header = {
    	# 'Accept': 'application/json',
    	# 'Content-Type': 'application/json',
    	# 'X-BTK-APIKEY': API_KEY,
        # }
        # data = {
        #     'ts': getServerTime(),
        # }
        # signature = sign(data)
        # data['sig'] = signature
        # print('Payload with signature: ' + json_encode(data))
        response = requests.get(self.API_HOST + '/api/market/ticker?sym='+_sym)
        data = response.json()
        #data = data['result']
        # print(response.json())
        return(data)
       
    
    def rebalance(self,_pair , _token_name , _target , _OrderActivate , _gap):
        returnText = ''
        pair = _pair#'THB_KUB' #เหรียญ
        token_name =_token_name #'KUB' #เหรียญ
    
        balance_coin=self.balances()
        balance_coin=balance_coin['result'][token_name]['available'] + balance_coin['result'][token_name]['reserved']
        #print('จำนวนเหรียญในบัญชี' , balance_coin , 'เหรียญ')
    
        balance_thb=self.balances()
        balance_thb=balance_thb['result']['THB']['available'] + balance_thb['result']['THB']['reserved']
        #print('จำนวนเงินในบัญชี' , balance_thb , 'บาท')
    
        last_price = self.ticker(pair)
        last_price = last_price[pair]['last']
        #print('ราคาเหรียญล่าสุด' , last_price , 'บาท')
    
        balance_value = balance_coin*last_price
        #print('มูลค่าเหรียญ' ,  balance_value , 'บาท')
    
        port = balance_thb + balance_value
        # portfolio = 'มูลค่าพอร์ต  {:,.2f}  บาท'.format(port)
        # print('มูลค่าพอร์ต' , portfolio , 'บาท')
    
        fix_value = _target #ใส่จำนวนเงินที่ต้องการrebalance
        amount = balance_value - fix_value
        # print(balance_value , ': balance_value <> fix_value :',fix_value , ' amount :' , amount)
        if balance_value > fix_value:
            amount = balance_value - fix_value
            amountToSell = amount / last_price
            # print(amount)
            if amount > 10: #มูลค่าเพิ่มมากกว่าเท่าไหร่ถึงจะแจ้งเตือน
                # print('ขายออก' , amount , 'บาท')
                #print(type(amount))
                #messenger.sendtext('Sell ' + str(float(amount)) +' Baht')
                # sendLine('{} Sell {:,.2f} baht @ {:,.2f} '.format(_pair,amount,last_price))
                if _OrderActivate == True:
                    self.sell(_pair,amountToSell,last_price)
                returnText =  '{} Sell {:,.2f} baht @ {:,.2f} '.format(_pair,amount,last_price)
            else:
                # print('Rebalance : Waiting')
                returnText = 'Rebalance : Waiting'
            # messenger.sendtext('Rebalance : Waiting')
        elif balance_value < fix_value:
            amount = fix_value - balance_value
            # print(amount)
            if amount > 10: #มูลค่าลดมากกว่าเท่าไหร่ถึงจะแจ้งเตือน
                # print('ซื้อเข้า' , amount , 'บาท')
                # sendLine('{} Buy {:,.2f} baht @ {:,.2f} '.format(_pair,amount,last_price))
                if _OrderActivate == True:
                    self.buy(_pair,amount,last_price)
                returnText =  '{} Buy {:,.2f} baht @ {:,.2f} '.format(_pair,amount,last_price)
            else:
                # print('Rebalance : Waiting')
                returnText = 'Rebalance : Waiting'
                #messenger.sendtext('Rebalance : Waiting')
        else:
            # print('Not yet')
            returnText = 'Not yet'
        return returnText
    
    def trand_ema(self, symbol, df, fast_length=9, slow_length=26, export_limit=7, export_full=False):
        SIGNAL          = None
        TREND           = None
        EMA_FAST_A      = 0
        EMA_FAST_B      = 0
        EMA_SLOW_A      = 0
        EMA_SLOW_B      = 0
        AVG_MIN         = 0 
        
        if len(df) >= 3:
            if len(df) < slow_length:
                df_length = (len(df) - 1)
                EMA_FAST_A = df['close'][df_length]
                EMA_FAST_B = df['close'][df_length - 2]

                EMA_SLOW_A = df['close'][df_length]
                EMA_SLOW_B = df['close'][df_length - 2]

                df_ohlcv   = df


            else:
                # print(f"trend up {fast_length} {slow_length}")
                # เรียกโมดูล EMS
                EMA_FAST = df.ta.ema(fast_length)
                EMA_SLOW = df.ta.ema(slow_length)

                ## เพิ่มคอลั่ม EMA
                data = pd.concat([df, EMA_FAST], axis=1)
                df_ohlcv = pd.concat([data, EMA_SLOW], axis=1)

                df_length = (len(df_ohlcv) - 1)
                EMA_FAST_A = df_ohlcv['EMA_' + str(fast_length)][df_length]
                EMA_FAST_B = df_ohlcv['EMA_' + str(fast_length)][df_length - 2]

                EMA_SLOW_A = df_ohlcv['EMA_' + str(slow_length)][df_length]
                EMA_SLOW_B = df_ohlcv['EMA_' + str(slow_length)][df_length - 2]


            SIGNAL = None
            TREND = None

            if EMA_FAST_A > EMA_SLOW_A:
                TREND = "UP"

            elif EMA_FAST_A < EMA_SLOW_A:
                TREND = "DOWN"

            if EMA_FAST_A > EMA_SLOW_A and EMA_FAST_B > EMA_SLOW_B:
                SIGNAL = "BUY"

            elif EMA_FAST_A < EMA_SLOW_A and EMA_FAST_B < EMA_SLOW_B:
                SIGNAL = "SELL"

            print("\n" + colored(''.rjust(60, '+'), 'yellow') + "\n")  
            print("SYM :=> ", colored(symbol, 'yellow'), colored(symbol, 'yellow'))
            print("EMA FAST :=> ", colored(EMA_FAST_A, 'red'), colored(EMA_FAST_B, 'blue'))
            print("EMA SLOW :=> ", colored(EMA_SLOW_A, 'red'), colored(EMA_SLOW_B, 'blue'))

            txtcolor_trend = "green"
            if TREND == "DOWN": txtcolor_trend = "red"
            
            txtcolor_signal = "green"
            if SIGNAL == "SELL": txtcolor_signal = "red"


            print("TREND :=> ", colored(TREND, txtcolor_trend))
            print("SIGNAL :=> ", colored(SIGNAL, txtcolor_signal))

            AVG_FAST = float((EMA_FAST_A+EMA_FAST_B)/2)
            AVG_SLOW = float((EMA_SLOW_A+EMA_SLOW_B)/2)

            print("\n")
            print("AVG FAST :=> ", colored(AVG_FAST, 'red'))
            print("AVG SLOW :=> ", colored(AVG_SLOW, 'red'))

            AVG_MIN = (AVG_FAST - AVG_SLOW)
            print("AVG MINUS :=> ", colored(AVG_MIN, 'blue'))
            print("\n" + colored(''.rjust(60, '+'), 'yellow'))


            # export_path = f"exports/excels/trends"
            # if not os.path.exists(export_path):
            #     os.makedirs(export_path)

            # filename = f"{export_path}/EMA.{fast_length}.{slow_length}.{symbol}.{datetime.datetime.now().strftime('%Y%m%d')}.xlsx"

            # if len(df_ohlcv) > 0:
            #     if export_full:
            #         df_ohlcv.to_excel(filename)

            #     else:
            #         obj = df_ohlcv.tail(export_limit)
            #         obj.to_excel(filename)

            
        return {
            # 'data': df_ohlcv,
            'key': str(uuid4()),
            "asset": symbol,
            'trend': TREND,
            'signal': SIGNAL,
            'last_fast': float(format(EMA_FAST_A,'.2f')),
            'old_fast': float(format(EMA_FAST_B,'.2f')),
            'last_slow': float(format(EMA_SLOW_A,'.2f')),
            'old_slow': float(format(EMA_SLOW_B,'.2f')),
            'avg_fast': float(format((EMA_FAST_A+EMA_FAST_B)/2,'.2f')),
            'avg_slow': float(format((EMA_SLOW_A+EMA_SLOW_B)/2,'.2f')),
            'avg': float(format(AVG_MIN,'.2f')),
            'lastupdate': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
    
    
    
    def get_candle(self, symbol="ZIL", timeframe="1D"):
        # เรียก ข้อมูลราคา ของสินค้ามาไว้ในรูปแบบ ตาราง
        # กำหนดตัวแปร ที่ต้องใช้
        # timeframe = ช่วงเวลาของกราฟที่จะดึงข้อมูล 1, 5, 15, 60, 240, 1D
        timestramp = self.timeserver()
        form_time = datetime.datetime.fromtimestamp(
            timestramp) - datetime.timedelta(days=self.API_LIMIT)

        if (timeframe).find("D") < 0:
            form_time = datetime.datetime.fromtimestamp(
                timestramp) - datetime.timedelta(minutes=(int(timeframe) * self.API_LIMIT))

        to_date = datetime.datetime.fromtimestamp(timestramp)
        # msg = f"ดึงข้อมูลกราฟ {colored(symbol +'-'+self.API_CURRENCY, 'blue')} จากวันที่ {(colored(form_time, 'blue'))} ถึง {colored(to_date, 'blue')}"
        # print(msg)
        # # เรียก ข้อมูล จาก  exchange
        url = f"{self.API_HOST}/tradingview/history?symbol={symbol}_{self.API_CURRENCY}&resolution={timeframe}&from={int((form_time).timestamp())}&to={int((to_date).timestamp())}"
        response = requests.get(url, headers={}, data={})
        candles = response.json()
        # # เรียงให้เป็น ตาราง + เอามาจัดเรียง ใส่หัวข้อ
        df = pd.DataFrame(
            candles, columns=['t', 'o', 'c', 'h', 'l', 'v'])

        # # แปลงรูปแบบ ของเวลา ด้วย Pandas
        df['t'] = pd.to_datetime(df['t'], unit='s')
        data = df.rename({'t': 'datetime', 'o': 'open',
                        'c': 'close', 'h': 'high', 'l': 'low', 'v': 'volume'}, axis=1)
        
        ### บันทึกข้อมูลเป็น excel
        export_path = f"exports/excels/assets/{symbol}"
        if not os.path.exists(export_path):
            os.makedirs(export_path)
            
        # filename = f"{export_path}/{timeframe}.{datetime.datetime.now().strftime('%Y%m%d')}.xlsx"
        # data.to_excel(filename)
        ##  ------>
        
        # print(data.tail())
        return data , url
    
    def get_candle_dataframe(self, symbol="ZIL", timeframe="1D"):
        # เรียก ข้อมูลราคา ของสินค้ามาไว้ในรูปแบบ ตาราง
        # กำหนดตัวแปร ที่ต้องใช้
        # timeframe = ช่วงเวลาของกราฟที่จะดึงข้อมูล 1, 5, 15, 60, 240, 1D
        timestramp = self.timeserver()
        form_time = datetime.datetime.fromtimestamp(
            timestramp) - datetime.timedelta(days=self.API_LIMIT)

        if (timeframe).find("D") < 0:
            form_time = datetime.datetime.fromtimestamp(
                timestramp) - datetime.timedelta(minutes=(int(timeframe) * self.API_LIMIT))

        to_date = datetime.datetime.fromtimestamp(timestramp)
        # msg = f"ดึงข้อมูลกราฟ {colored(symbol +'-'+self.API_CURRENCY, 'blue')} จากวันที่ {(colored(form_time, 'blue'))} ถึง {colored(to_date, 'blue')}"
        # print(msg)
        # # เรียก ข้อมูล จาก  exchange
        url = f"{self.API_HOST}/tradingview/history?symbol={symbol}_{self.API_CURRENCY}&resolution={timeframe}&from={int((form_time).timestamp())}&to={int((to_date).timestamp())}"
        response = requests.get(url, headers={}, data={})
        candles = response.json()
        # # เรียงให้เป็น ตาราง + เอามาจัดเรียง ใส่หัวข้อ
        df = pd.DataFrame(
            candles, columns=['t', 'o', 'c', 'h', 'l', 'v'])

        # # แปลงรูปแบบ ของเวลา ด้วย Pandas
        df['t'] = pd.to_datetime(df['t'], unit='s')
        data = df.rename({'t': 'datetime', 'o': 'open',
                        'c': 'close', 'h': 'high', 'l': 'low', 'v': 'volume'}, axis=1)
        
        ### บันทึกข้อมูลเป็น excel
        # export_path = f"exports/excels/assets/{symbol}"
        # if not os.path.exists(export_path):
        #     os.makedirs(export_path)
            
        # filename = f"{export_path}/{timeframe}.{datetime.datetime.now().strftime('%Y%m%d')}.xlsx"
        # data.to_excel(filename)
        # ##  ------>
        
        # print(data.tail())
        return data
    
    def STOCHRSIsignal(self , df, symbol, rsi_period = 26, stoch_period = (5, 3), levels = (30, 70) ):
        """
        :input: ohlcv DataFrame, pd.DataFrame
                period, int
        
        :return: STOCHRSI value,
                 STOCHRSI uptrend,
                 STOCHRSI downtrend,
                 
        StochRSI is an indicator of an indicator, which makes it the 
        second derivative of price. This means it is two steps (formulas) 
        removed from the price of the underlying security. Price has 
        undergone two changes to become StochRSI. Converting prices to RSI 
        is one change. Converting RSI to the Stochastic Oscillator is 
        the second change. This is why the end product (StochRSI) looks 
        much different than the original (price). 
        
        """
        # set kwargs
        kwargs = { 'timeperiod'   : rsi_period, 
                   'fastk_period' : stoch_period[0], 
                   'fastd_period' : stoch_period[1], 
                   'fastd_matype' : 1,
                  }
        
        df['FASTk'], df['FASTd'] = talib.STOCHRSI(df['close'], **kwargs)
        stoch_rsi_value = df['FASTd'].values[-1]
        up_trend = (stoch_rsi_value > levels[1]).astype(int)
        down_trend = (stoch_rsi_value < levels[0]).astype(int) 
        SIGNAL = 'Hold'
        SignalDesc = 'นิ่งไว้ไอ้เสือ'
        if stoch_rsi_value <= 10:
            SIGNAL = 'Buy'
            SignalDesc = 'หลุมครับหลุม ซื้อเลย หลุมครับ'
        if stoch_rsi_value >= 80:
            SIGNAL = 'Sell'
            SignalDesc = 'ขายเลยลูก เนิน นั่น เนิน'
        return {
            # 'data': df_ohlcv,
            'key': str(uuid4()),
            "asset": symbol,
            'STOCHRSIk': float(format(stoch_rsi_value,'.2f')),
            'signal': SIGNAL,
            'SignalDesc': SignalDesc,
            'STOCHRSI OverBougth':float(format(up_trend,'.2f')),
            'STOCHRSI OverSold': float(format(down_trend,'.2f')),
            'lastupdate': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        # return {'STOCHRSIk' : stoch_rsi_value, 'STOCHRSI OverBougth' : up_trend, 'STOCHRSI OverSold' : down_trend,}
    
    def MACDsignal(self , df , symbol , fast = 12, slow = 26, signal = 9 , timeframe = 5):
    
        """
        :input: ohlcv DataFrame, pd.DataFrame
                period, int
        
        :return: MACD value,
                 MACD hist value,
                 MACD value label
                 MACD hist label
        
        The moving average convergence divergence (MACD) indicator helps 
        traders see the trend direction, as well as the momentum of that trend. 
        It also provide a number of trade signals.
        When the MACD is above zero, the price is in an upward phase. 
        If the MACD is below zero, it has entered a bearish period.
        
        The indicator is composed of two lines: the MACD line and a signal line, 
        which moves slower. When MACD crosses below the signal line, 
        it indicates that the price is falling. When the MACD line crosses 
        above the signal line, the price is rising. 
        
        Looking at which side of zero the indicator is on aids in determining 
        which signals to follow. For example, if the indicator is above zero, 
        watch for the MACD to cross above the signal line to buy. 
        If the MACD is below zero, the MACD crossing below the signal line may 
        provide the signal for a possible short trade. 
        
        """
        
        
        # set kwargs
        kwargs = {'fastperiod'    : fast,
                  'slowperiod'    : slow,
                  'signalperiod'  : signal, 
                  }
        
        df['MACD'], _ , df['MACDhist'] = talib.MACD(df['close'], **kwargs)
       
        # calc close mean
        n = 3
        price = df['close'][-(slow+n):]
        # select valleys
        valleys = price[(price.diff() > 0).astype(int).diff() == -1]
        # calculate uptrend
        price_lr = np.polyfit(range(len(valleys.index)), valleys.values, 1)            
        # macd values to evaluate
        macd_value = df['MACD'].values[-1]
        macd_hist = df['MACDhist'].values[-1]
        
        # check valleys going higher
        if price_lr[0] > 0:
            
            if macd_value > 0:    
                value_label = 1 # buy
            else:
                value_label = 0 # not Buy
            
            if macd_hist > 0:
                signal_label = 1 # buy
            else:
                signal_label = 0 # not buy
            
        else:
            value_label = 0 # sell
            signal_label = 0 # sell
        
        label_0 = f'MACD({fast}, {slow}, {signal}) value'
        label_1 = f'MACD({fast}, {slow}, {signal}) hist'
        label_2 = f'MACD({fast}, {slow}, {signal}) value signal'
        label_3 = f'MACD({fast}, {slow}, {signal}) hist signal'
        signal = 'เฉยไว้ไอ้หนู'
        if signal_label == 0 and value_label == 0:
            signal = 'ขายเลยลูก เนิน นั่น เนิน'
        elif signal_label == 1 and value_label ==1:
            signal = 'ซื้อลูกให้ไว หลุม'
        else:
            signal = 'เฉยไว้ไอ้หนู'
        return {
            # 'data': df_ohlcv,
            'key': str(uuid4()),
            "asset": symbol,
            label_0 : macd_value,
            label_1 : macd_hist,
            label_2 : value_label,
            label_3 : signal_label,
            "macd_value":{label_0 : macd_value},
            "macd_hist":{label_1 : macd_hist},
            "value_label":{label_2 : value_label},
            "signal_label":{label_3 : signal_label},
            'signal':signal,
            'lastupdate': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        # return {label_0 : macd_value, label_1 : macd_hist, label_2 : value_label, label_3 : signal_label}
    
   
    # def main(self):
        # s.enter(1, 1,  calc, (s,))
# bugkub = BugKib()
# bugkub.calc()
        # dataPrice = getAllPrice()
        # allText = ''
        # for c in MyWatcher:
        #     sym = c
            # rebalance('THB_'+sym,sym,rebalanceTarget['THB_'+sym])
            # data = dataPrice['THB_'+sym]
            # last = data['last']
            # CheckCondition(sc=None,coin='THB_'+sym , price=last)
            # s.enter(5, 1, CheckCondition, kwargs={'sc':s,'coin': 'THB_'+sym,'price': last})
        # s.run()
        # print('-----')
        # exit()
        
        
            # time.sleep(60)
    
    
    # if __name__ == "__main__":
        # main(None)

