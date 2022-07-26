# -*- coding: utf-8 -*-


# import websocket
import json
import pandas as pd
import pickle
import talib
from datetime import datetime, timezone
import numpy
import os
from apibutkib import BugKib
from pymongo import MongoClient
import numpy as np
import time
import re
import math
# from pyspark.sql import functions as F
# from pyspark.sql import types as T
# from pyspark.sql import types as T
# from pyspark.sql.types import *
# from pyspark import SparkContext
# from pyspark.sql import SparkSession
client = MongoClient('mongodbAddress',27017)
db = client.bitkub
trend_db = db.trends
subscribe_db = db.subscribe
stochrsi_db = db.stochrsis
macd_db = db.macds
profitDb = db.profits
buyDb = db.buys
sellDb = db.sells
assetDb = db.assets
joblogDb = db.joblogs
cancleDb = db.cancleLogs
botActivateDb = db.botactivate
# spark = SparkSession.builder.getOrCreate()
botStopLossDb = db.botStopLoss
APIKEYBITKUB='APIKEY_BITKUB'
bitkub = BugKib(_apiKey=APIKEYBITKUB,_apisecret = b'APISECRET_BITKUB')
bitkubTa = BugKib(_apiKey='APIKEY_BITKUB',_apisecret = b'APISECRET_BITKUB')
symbol = 'KUB'
lastBuyPrice = bitkub.costBasisAveragePrice(symbol,timestamp=1656670957) # Saturday, June 25, 2022 12:30:00 PM GMT+07:00 
 # try:
 #     lastBuyPrice = bitkub.costBasisAveragePrice(symbol,timestamp=1655446223)
if(math.isnan(lastBuyPrice)):
    lastBuyPrice = bitkub.getLastBuyAverage(symbol)

# lineOrderToken = 'LINENOTIFYTOKEN'
# # lineSignalToken = 'LINENOTIFYTOKEN'
# lineSignalToken = 'LINENOTIFYTOKEN'
# symbol = 'GALA'
# _pair='THB_'+symbol
# lastBuyPrice = bitkub.costBasisAveragePrice(symbol,timestamp=1656135000)
# _rat = bitkub.get_last_price(_pair)
# _PercentToSell = 99
# _textSellDescription = 'ขายทิ้ง Stop Loss ที่ขาดทุน :' + str('9')
# sellResponse = bitkub.sellMarket(_pair,68, _rat['last']  ,lineOrderToken,'ขายทิ้ง Stop Loss ที่ขาดทุน :' + str('aProfitWithFee'))
# sellResponse = json.loads(sellResponse.text)
# sellResponse = sellResponse['result']
# botStopLossDbSave   = {
#         "hash": str(sellResponse['hash']),
#         "key": str("TEST"),
#         "Asset": symbol,
#         "Signal": '_signal',
#         "StochRSI": '_STOCHRSIk',
#         "AssetInTHB":'balance_value',
#         "AvgBuyPrice":'lastBuyPrice',
#         "SellPrice":_rat['last'],
#         "Available":'Available',
#         "Amount":1,
#         "PercentToSell" : _PercentToSell,
#         "Reserved":1,
#         "Profit":1,
#         "ProfitGoal":1,
#         "Description":_textSellDescription,
#         "AmountToBuy":sellResponse['amt'],
#         "Type":sellResponse['typ'],
#         "Fee":sellResponse['fee'],
#         "CreditFee":sellResponse['cre'],
#         "AmountToReceive":sellResponse['rec'],
#         "timestamp":sellResponse['ts'],
#         "LastUpdate": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#     }
# botStopLossDb[APIKEYBITKUB].insert_one(botStopLossDbSave)
# # lastBuyPrice = bitkub.costBasisAveragePrice(symbol,timestamp=1656135000)
# # lastBuyPrice_OLD = bitkub.getLastBuyAverage(symbol)
# dt = round(datetime.now().today().timestamp())

  # if (timeframe).find("D") < 0:
  #     form_time = datetime.datetime.fromtimestamp(
  #         timestramp) - datetime.timedelta(minutes=(int(timeframe) * self.API_LIMIT))


# tradeLists = {'NEAR','KUB','ADA','DOGE'}
# tradeOption = {
#             'DEFAULT':{'Buy':50,'Sell':295,'MaxAmt':150,'firstInitial':50,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
#             'GT':{'Buy':50,'Sell':295,'MaxAmt':150,'firstInitial':50,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
#             'KUB':{'Buy':200,'Sell':295,'MaxAmt':600,'firstInitial':200,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
#             'ADA':{'Buy':200,'Sell':295,'MaxAmt':600,'firstInitial':200,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
#             'CHZ':{'Buy':250,'Sell':295,'MaxAmt':500,'firstInitial':250,'timeframe':'5','profitTotake':15,'tradeStyle':'stepProfit'},
#             'GRT':{'Buy':250,'Sell':295,'MaxAmt':500,'firstInitial':250,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
#             'MANA':{'Buy':50,'Sell':295,'MaxAmt':150,'firstInitial':50,'timeframe':'5','profitTotake':5,'tradeStyle':'stepProfit'},
#             'BNB':{'Buy':50,'Sell':594,'MaxAmt':150,'firstInitial':100,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
#             'ALPHA':{'Buy':50,'Sell':295,'MaxAmt':150,'firstInitial':50,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
#             'SOL':{'Buy':50,'Sell':195,'MaxAmt':150,'firstInitial':50,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
#             'GALA':{'Buy':50,'Sell':195,'MaxAmt':150,'firstInitial':50,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
#             'SUSHI':{'Buy':50,'Sell':195,'MaxAmt':150,'firstInitial':50,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
#             'BTC':{'Buy':50,'Sell':495,'MaxAmt':150,'firstInitial':200,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
#             'NEAR':{'Buy':500,'Sell':495,'MaxAmt':1000,'firstInitial':500,'timeframe':'5','profitTotake':20,'tradeStyle':'stepProfit'},
#             'APE':{'Buy':50,'Sell':495,'MaxAmt':150,'firstInitial':50,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
#             'ETH':{'Buy':50,'Sell':495,'MaxAmt':150,'firstInitial':50,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
#             'JFIN':{'Buy':50,'Sell':495,'MaxAmt':150,'firstInitial':50,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
#             'FTM':{'Buy':50,'Sell':495,'MaxAmt':150,'firstInitial':50,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
#             'DOGE':{'Buy':200,'Sell':495,'MaxAmt':2200,'firstInitial':200,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
#             }
# tradeStyleStep = {  # SYMBOL : {'RSI':'PERCENT TO SELL'}
#                      'DEFAULT':{
#                                   'Range':{'Min':30,'Max':40,'PercentToSell':20},
#                                   'Range2':{'Min':40,'Max':50,'PercentToSell':30},
#                                   'Range3':{'Min':50,'Max':60,'PercentToSell':40},
#                                   'Range4':{'Min':60,'Max':70,'PercentToSell':50},
#                                   'Range5':{'Min':70,'Max':80,'PercentToSell':60},
#                                   'Range6':{'Min':80,'Max':90,'PercentToSell':80},
#                                   'Range7':{'Min':90,'Max':100,'PercentToSell':99}
#                          },
                          
#                      'BTC':{
#                              'Range':{'Min':30,'Max':40,'PercentToSell':20},
#                              'Range2':{'Min':40,'Max':50,'PercentToSell':30},
#                              'Range3':{'Min':50,'Max':60,'PercentToSell':40},
#                              'Range4':{'Min':60,'Max':70,'PercentToSell':50},
#                              'Range5':{'Min':70,'Max':80,'PercentToSell':60},
#                              'Range6':{'Min':80,'Max':90,'PercentToSell':80},
#                              'Range7':{'Min':90,'Max':100,'PercentToSell':99}
#                          },
                     
#                      'BNB':{
#                              'Range':{'Min':30,'Max':40,'PercentToSell':20},
#                              'Range2':{'Min':40,'Max':50,'PercentToSell':30},
#                              'Range3':{'Min':50,'Max':60,'PercentToSell':40},
#                              'Range4':{'Min':60,'Max':70,'PercentToSell':50},
#                              'Range5':{'Min':70,'Max':80,'PercentToSell':60},
#                              'Range6':{'Min':80,'Max':90,'PercentToSell':80},
#                              'Range7':{'Min':90,'Max':100,'PercentToSell':99}
#                          },
                     
#                      'GT':{
#                              'Range':{'Min':30,'Max':40,'PercentToSell':20},
#                              'Range2':{'Min':40,'Max':50,'PercentToSell':30},
#                              'Range3':{'Min':50,'Max':60,'PercentToSell':40},
#                              'Range4':{'Min':60,'Max':70,'PercentToSell':50},
#                              'Range5':{'Min':70,'Max':80,'PercentToSell':60},
#                              'Range6':{'Min':80,'Max':90,'PercentToSell':80},
#                              'Range7':{'Min':90,'Max':100,'PercentToSell':99}
#                          },
#                      'MANA':{
#                              'Range':{'Min':30,'Max':40,'PercentToSell':20},
#                              'Range2':{'Min':40,'Max':50,'PercentToSell':30},
#                              'Range3':{'Min':50,'Max':60,'PercentToSell':40},
#                              'Range4':{'Min':60,'Max':70,'PercentToSell':50},
#                              'Range5':{'Min':70,'Max':80,'PercentToSell':60},
#                              'Range6':{'Min':80,'Max':90,'PercentToSell':80},
#                              'Range7':{'Min':90,'Max':100,'PercentToSell':99}
#                          },
#                      'ALPHA':{
#                              'Range':{'Min':30,'Max':40,'PercentToSell':20},
#                              'Range2':{'Min':40,'Max':50,'PercentToSell':30},
#                              'Range3':{'Min':50,'Max':60,'PercentToSell':40},
#                              'Range4':{'Min':60,'Max':70,'PercentToSell':50},
#                              'Range5':{'Min':70,'Max':80,'PercentToSell':60},
#                              'Range6':{'Min':80,'Max':90,'PercentToSell':80},
#                              'Range7':{'Min':90,'Max':100,'PercentToSell':99}
#                          },
#                      'SOL':{
#                              'Range':{'Min':30,'Max':40,'PercentToSell':20},
#                              'Range2':{'Min':40,'Max':50,'PercentToSell':30},
#                              'Range3':{'Min':50,'Max':60,'PercentToSell':40},
#                              'Range4':{'Min':60,'Max':70,'PercentToSell':50},
#                              'Range5':{'Min':70,'Max':80,'PercentToSell':60},
#                              'Range6':{'Min':80,'Max':90,'PercentToSell':80},
#                              'Range7':{'Min':90,'Max':100,'PercentToSell':99}
#                          },
#                      'GALA':{
#                              'Range':{'Min':30,'Max':40,'PercentToSell':20},
#                              'Range2':{'Min':40,'Max':50,'PercentToSell':30},
#                              'Range3':{'Min':50,'Max':60,'PercentToSell':40},
#                              'Range4':{'Min':60,'Max':70,'PercentToSell':50},
#                              'Range5':{'Min':70,'Max':80,'PercentToSell':60},
#                              'Range6':{'Min':80,'Max':90,'PercentToSell':80},
#                              'Range7':{'Min':90,'Max':100,'PercentToSell':99}
#                          },
#                      'SUSHI':{
#                              'Range':{'Min':30,'Max':40,'PercentToSell':20},
#                              'Range2':{'Min':40,'Max':50,'PercentToSell':30},
#                              'Range3':{'Min':50,'Max':60,'PercentToSell':40},
#                              'Range4':{'Min':60,'Max':70,'PercentToSell':50},
#                              'Range5':{'Min':70,'Max':80,'PercentToSell':60},
#                              'Range6':{'Min':80,'Max':90,'PercentToSell':80},
#                              'Range7':{'Min':90,'Max':100,'PercentToSell':99}
#                          },
#     }
# try:
#     botActivate = { "Instance": APIKEYBITKUB }
#     botActivateDoc = botActivateDb.find_one(botActivate)
#     Stop_Loss_at_Money = botActivateDoc['Stop_Loss_at_Money']
#     tradeOptions_mongo = botActivateDoc['tradeOptions']
#     tradeStyleSteps_mongo = botActivateDoc['tradeStyleSteps']
#     tradeLists_mongo = botActivateDoc['tradeLists']
#     if(botActivateDoc['Activate']==False):
#         logSave   = {
#                 "CASH": bitkub.getMyMoney(),
#                 "Asset": "BOT IS DEACTIVATE",
#                 "Signal": "BOT IS DEACTIVATE",
#                 "StochRSI": "BOT IS DEACTIVATE",
#                 "AssetInTHB":"BOT IS DEACTIVATE",
#                 "AvgBuyPrice":"BOT IS DEACTIVATE",
#                 "CurrentPrice":"BOT IS DEACTIVATE",
#                 "Available":"BOT IS DEACTIVATE",
#                 "Reserved":"BOT IS DEACTIVATE",
#                 "Profit":"BOT IS DEACTIVATE",
#                 "ProfitGoal":"BOT IS DEACTIVATE",
#                 "LastUpdate": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#             }
#         joblogDb[APIKEYBITKUB].insert_one(logSave)
#         botActivateDb.update_one({'Instance': APIKEYBITKUB},
#                    {'$set': {'Activate': False}
#                     }
#                    ,upsert=True
#                    )
#         bitkub.sendLine('Stop Loss บอทไม่ทำงาน เพราะตั้ง Stop Loss ไว้ที่ : ' + str(Stop_Loss_at_Money) + ' \n เงินคุณมี : '+ str(bitkub.getMyMoney()),token=lineOrderToken)
#         sys.exit("BOT IS DEACTIVATE")
# except KeyError:
#     botActivateDb.update_one(
#         {'Instance': APIKEYBITKUB},
#                 {
#                     '$set': {
#                         'tradeOptions': tradeOption,
#                         'tradeStyleSteps':tradeStyleStep,
#                         'tradeLists':list(tradeLists)
#                         }
#                 },upsert=True
#                 )
#     botActivate = { "Instance": APIKEYBITKUB }
#     botActivateDoc = botActivateDb.find_one(botActivate)
#     tradeOptions_mongo = botActivateDoc['tradeOptions']
#     tradeStyleSteps_mongo = botActivateDoc['tradeStyleSteps']
#     tradeLists_mongo = botActivateDoc['tradeLists']
    
# except Exception:
#     pass

# if(math.isnan(lastBuyPrice)):
#     lastBuyPrice = bitkub.getLastBuyAverage(symbol)
# if(math.isnan(d)):
#     d = bitkub.getLastBuyAverage(symbol)
# a='Beautiful, is; better*than\nugly sss'

# t = re.split('; |, |\*|\n| ',a)
# aaa = t[0]

# bal,aDataTa = bitkubTa.get_balance_assets()
# bal,aData = bitkub.get_balance_assets()
# # aBigData = {}
# lastbuyPriceTa = {}
# lastbuyPriceToei = {}
# NanTa = {}
# NanToei= {}
# tradeLists = {'FTM','SOL','DOGE','ZIL','KUB','BNB','NEAR'}



# res = bitkub.get_wallets_assets()
# # b = a['result']

# if res['error'] == 0:
#     currency = res['result']
#     result = ''
#     for i in currency:
#         ccc = currency.get(i)
#         if ccc > 0 :
#             result += str(i) + ' : ' + str(ccc ) +'\n'
#             # result += ''
# # for ba in aDataTa['result']:
# #     symbol = ba
# #     if(symbol=='THB' or symbol=='DON' or symbol=='LUNA2' ):
#         # if(ba['symbol']=='THB'):
#             # cash = ba['available']
#             # aBigData[symbol] = {'money':ba['available']}
#         pass
#     else:
#         # lastBuyPrices = {}
        
#         _pair = 'THB_'+symbol
#         # _rat = bitkub.get_last_price(_pair)
#         # _ratBTC = bitkub.get_last_price('THB_BTC')
#         # aOrderHistory[_pair] = bitkub.get_order_history(_pair)
#         #aBigData[symbol] , _  = bitkub.get_candle(symbol, timeframe='60')
#         # lastBuyPrice = bitkubTa.costBasisAveragePrice(symbol,timestamp=1655446223)
        
#         try:
#             lastbuyPriceTa[symbol] = bitkubTa.costBasisAveragePrice(symbol,timestamp=1655446223)
#             if(math.isnan(lastbuyPriceTa[symbol])):
#                 NanTa[symbol] = lastbuyPriceTa[symbol]
#                 lastbuyPriceTa[symbol] = bitkubTa.costBasisAveragePrice(symbol)
#           #   print(sym , " : lastBuyPrice ",lastBuyPrice)
#         except:
#             lastbuyPriceTa[symbol] = 0.0000
       
# for ba in aData['result']:
#     symbol = ba
#     if(symbol=='THB' or symbol=='DON' or symbol=='LUNA2' ):
#         # if(ba['symbol']=='THB'):
#             # cash = ba['available']
#             # aBigData[symbol] = {'money':ba['available']}
#         pass
#     else:
#         # lastBuyPrices = {}
        
#         _pair = 'THB_'+symbol
#         # _rat = bitkub.get_last_price(_pair)
#         # _ratBTC = bitkub.get_last_price('THB_BTC')
#         # aOrderHistory[_pair] = bitkub.get_order_history(_pair)
#         #aBigData[symbol] , _  = bitkub.get_candle(symbol, timeframe='60')
#         # lastBuyPrice = bitkubTa.costBasisAveragePrice(symbol,timestamp=1655446223)
        
#         try:
#             lastbuyPriceToei[symbol] = bitkub.costBasisAveragePrice(symbol,timestamp=1655446223)
#             if(math.isnan(lastbuyPriceToei[symbol])):
#                 NanToei[symbol] = lastbuyPriceToei[symbol]
#                 lastbuyPriceToei[symbol] = bitkub.costBasisAveragePrice(symbol)
#           #   print(sym , " : lastBuyPrice ",lastBuyPrice)
#         except:
#             lastbuyPriceToei[symbol] = 0.0000
       
        
# daBigData = pd.DataFrame(
#     aBigData
#     )
# bbb = aBigDatapan
# df = spark.createDataFrame(aBigData)
# df.show(truncate = False)
# UDF = F.udf(lambda z:bitkub.STOCHRSIsignal(aBigData, aBigData.keys())(z))
            
# df.withColumn("RSI", bitkub.STOCHRSIsignal(col("close"))) \
#    .show(truncate=False)
# dataFrameCandle = aBigData['ADA']['candle'][0]
# a = bitkub.STOCHRSIsignal(MyDataFrame,symbol)
# APIKEYBITKUB='APIKEY_BITKUB'
# bitkub = BugKib(_apiKey=APIKEYBITKUB,_apisecret = b'APISECRET_BITKUB')
# symbol = 'ZIL'
# lastBuyPrice = bitkub.costBasisAveragePrice(symbol)



# def costBasisAveragePrice(symbol):
#     a = bitkub.get_order_history('THB_'+symbol,555,1653436800,round(time.time()))
#     df = pd.DataFrame(
#         a, columns=['side', 'type', 'rate', 'fee', 'credit', 'amount','ts']
#         )

#     df['ts'] = pd.to_datetime(df['ts'], unit='s')
#     df = df.rename({'ts': 'datetime'}, axis=1)
#     df = df.sort_values(by="datetime")
#     df['Ticker'] = symbol
#     df['amount'] =pd.to_numeric(df['amount'], downcast='float')
#     df['rate'] = pd.to_numeric(df['rate'], downcast='float')
#     df['fee'] = pd.to_numeric(df['fee'], downcast='float')
#     df['credit'] = pd.to_numeric(df['credit'], downcast='float')
#     df['THB_InStock']=df['amount']  * df['rate'] 
#     df['TotalQty'] = df['amount'].where(df['side'].eq('buy'), -df['amount']).cumsum()
#     df['TotalQty'] = df['TotalQty'].apply(lambda x: float('%.10f' % x))
#     df1 = (df.copy()[df['side'] == 'buy']
#        .assign(CumAmountBuy=df.groupby('Ticker')['THB_InStock'].cumsum())
#        .assign(CumQtyBuy=df.groupby('Ticker')['amount'].cumsum()))
#     df2 = pd.merge(df,df1,how='left',
#                     on=['datetime','side', 'Ticker', 'amount', 'rate', 
#                         'THB_InStock', 'TotalQty']).ffill()
#     s = df2['CumAmountBuy'] / df2['CumQtyBuy']
#     df2['AverageCost'] = np.select([((df2['side'] == 'buy') & (df2['side'].shift() == 'sell')),
#                              (df2['side'] == 'sell')],
#                            [((df2['amount'] * df2['rate'] + df2['TotalQty'].shift() * s.shift()) / df2['TotalQty']),
#                             np.nan],
#                            s)
#     df2['AverageCost'] = round(df2['AverageCost'],3).ffill()
#     df2 = df2.drop(['CumQtyBuy', 'CumAmountBuy'], axis=1)
#     return df2.loc[df2.index[-1], "AverageCost"]







# df['Adjusted Quantity'] = df.apply(lambda x: ((x.side == "buy") - (x.side == "sell")) * x['amount'], axis = 1)
# df['Adjusted Quantity'] = df.groupby('Ticker')['Adjusted Quantity'].cumsum()
# df['Adjusted Price Per Unit'] = df.apply(lambda x: ((x.side == "buy") - (x.side == "sell")) * x['THB_InStock'], axis = 1)
# df['Adjusted Price Per Unit'] = df['Adjusted Price Per Unit'].cumsum().div(df['TotalQty'])
# df['Adj'] = df.apply(lambda x: ((x.side == "Buy") - (x.side == "Sell")) * x['THB_InStock'], axis = 1)
# df['Adj'] = df.groupby('Ticker')['Adj'].cumsum().div(df['Adjusted Quantity'])
# df['THB_IF_SELL'] = df['TotalQty'].mul(df['Adjusted Price Per Unit'])

# df.loc[df['side'] == 'sell',['Adjusted Price Per Unit']] = np.NaN
# df.fillna(method='ffill', inplace=True)
# b = df.loc[df.index[-1], "Adjusted Price Per Unit"]










# def weighted_average(a, b, a_weight):
#     """Take an average of a and b, with a weighted by a_weight"""
#     # assert 0 <= a_weight <= 1
#     return a * a_weight + b * (1 - a_weight)

# def get_adjusted_price_for_ticker(single_ticker_df):
#     adjusted_price = 0
#     current_shares = 0
#     prices = []
#     for _, row in single_ticker_df.iterrows():
#         is_buy = row["side"] == "buy"
#         qtd = row["amount"]
#         if is_buy:
#             current_shares += qtd
#             cost_per_share = (qtd * row["rate"] + row["fee"]) / qtd
#             proportion_of_new_shares = qtd / current_shares
#             adjusted_price = weighted_average(cost_per_share, adjusted_price, proportion_of_new_shares)
#         else:
#             current_shares -= qtd
#         prices.append(adjusted_price)

#     single_ticker_df["Adjusted Price"] = prices
#     return single_ticker_df

# def get_adjusted_price(df):
#     return df.groupby("Ticker").apply(get_adjusted_price_for_ticker)



# bbb = get_adjusted_price(df)
