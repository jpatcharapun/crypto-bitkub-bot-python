# -*- coding: utf-8 -*-
from flask import Flask,request,json
import os , sys
from datetime import datetime
import json
import pandas as pd
import pickle
import talib
from datetime import datetime
import numpy
import os
import asyncio
import aiofiles
import pprint
import websocket as wb
from apibutkib import BugKib
from pymongo import MongoClient
import datetime
import sys
from termcolor import colored
import numpy as np
from uuid import uuid4
import math
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
import re

APIKEYBITKUB='APIKEY_BITKUB'
bitkub = BugKib(_apiKey=APIKEYBITKUB,_apisecret = b'APISECRET_BITKUB')
line_bot_api = LineBotApi('LINE BOT API')

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
botActivateDb = db.botactivate
lineLog = db.lineLog
lineOrderToken = 'LINENOTIFYTOKEN'
lineSignalToken = 'LINENOTIFYTOKEN'

app = Flask(__name__)
tb_name = datetime.datetime.now().strftime('%Y%m%d')

@app.route('/',methods=['POST','GET','PUT'])
def hello():
    try:
        data = request.json
        root = data['events'][0]
        replyToken = data['events'][0]['replyToken']
        incomingText = data['events'][0]['message']['text']
        who = root['source']['userId']
        resultText = ''
        conditionText_Bank = {'บช','บัญชี','ธนาคาร','Bank','Acc'}
        conditionText_Withdraw = {'wd','เงินออก','ถอน','เบิก'}
        conditionText_Price = {'ราคา','Price','rate','฿'}
        conditionText_Buy = {'buy','Buy','ซื้อ','เข้า'}
        conditionText_Sell = {'sell','Sell','ขาย','เข้า'}
        conditionText_OrderOpen = {'ดูออเดอร์','ออเดอร์','ord','order','open'}
        conditionText_CancelOrder = {'ยกเลิก','cancel'}
        conditionText_Wallet = {'wallet','เป๋า'}
        conditionText_Asset = {'asset','sum'}
        conditionText_BotRunCommand = {'runbot','startbot','เปิดบอท' ,'รันบอท'}
        conditionText_BotStopCommand= {'stopbot','pausebot','หยุดบอท' ,'ปิดบอท'}
        try:
            if re.split('; |, |\*|\n| |/|-',incomingText)[0] in conditionText_Withdraw:
                t = re.split('; |, |\*|\n| |/|-',incomingText)
                amount = t[1].strip()
                bank = bitkub.getBankAccount()
                a = bank['result']
                accountNo = a[0]['id']
                
                withdrawResult = bitkub.withdrawFiat(accountNo, amount, lineOrderToken)
                if(withdrawResult['error']==0):
                    line_bot_api.reply_message(replyToken, TextSendMessage(text='ถอนเงินสำเร็จ ไอ้สัส : '+str(amount) + '฿ ไปที่ : ' + str(accountNo)))
                    # line_bot_api.push_message(who, TextSendMessage(text='ถอนเงินสำเร็จ ไอ้สัส'))
                else:
                    # line_bot_api.push_message(who, TextSendMessage(text='ถอนเงิน Error : {} '.format(bitkub.errorCode[withdrawResult['error']])))
                    line_bot_api.reply_message(replyToken, TextSendMessage(text='ถอนเงิน Error : {} '.format(bitkub.errorCode[withdrawResult['error']])))
            elif incomingText in conditionText_Bank:
                bank = bitkub.getBankAccount()
                for s in bank['result']:
                    accountNo = s['id']
                    bankName = s['bank']
                    AccName = s['name']
                    Branch = s['branch']
                    resultText += 'บัญชี : ' + str(bankName) + '\nชื่อบัญชี : ' + str(AccName)  + '\nสาขา : ' + str(Branch)  + '\nเลข บช. : ' + str(accountNo) + '\n'
                line_bot_api.reply_message(replyToken, TextSendMessage(text=str(resultText)))
            # elif incomingText.split(',')[0]  in conditionText_Price:
            elif re.split('; |, |\*|\n| |/|-',incomingText)[0]  in conditionText_Price:
                # t = re.split('; |, |\*|\n| |/|-',incomingText)
                t = re.split('; |, |\*|\n| ',incomingText)
                _pair = 'THB_'+t[1].upper()
                _rat = bitkub.get_last_price(_pair)
                price = _rat['last']
                line_bot_api.reply_message(replyToken, TextSendMessage(text=str(t[1]+' ราคา :' + str(price) + '฿')))
            elif re.split('; |, |\*|\n| |/|-',incomingText)[0]  in conditionText_Asset:
                # t = re.split('; |, |\*|\n| |/|-',incomingText)
                t = re.split('; |, |\*|\n| ',incomingText)
                _pair = 'THB_'+t[1].upper()
                symbol = t[1].upper()
                lastBuyPrice ,df= bitkub.costBasisAveragePriceWithDF(symbol,timestamp=1656135000) # Saturday, June 25, 2022 12:30:00 PM GMT+07:00 
               
                # if(math.isnan(lastBuyPrice)):
                #     lastBuyPrice = bitkub.getLastBuyAverage(symbol)
                    
                line_bot_api.reply_message(replyToken, TextSendMessage(text=str(t[1]+' ราคา Buy:' + str(lastBuyPrice) + '฿' + '\n'+ df.to_string())))
            elif re.split('; |, |\*|\n| |/|-',incomingText)[0]  in conditionText_Buy:
                t = re.split('; |, |\*|\n| |/|-',incomingText)
                _pair = 'THB_'+t[1].upper()
                _amountTHB = t[2]
                _rat = bitkub.get_last_price(_pair)
                
                
                try:
                    price = t[3]
                    
                except IndexError :
                    price = _rat['last']
                
                buyResponse = bitkub.buy(_pair, _amountTHB , price,lineOrderToken)
                
                if(buyResponse['error']==0):
                    line_bot_api.reply_message(replyToken, TextSendMessage(text='สั่งซื้อ '+str(t[1])+' ที่ราคา : '+str(price)+'฿ ด้วยเงิน '+str(_amountTHB)+' สำเร็จ ไอ้สัส'))
                else:
                    line_bot_api.reply_message(replyToken, TextSendMessage(text='สั่งซื้อ Error : {} '.format(bitkub.errorCode[buyResponse['error']])))
                # line_bot_api.reply_message(replyToken, TextSendMessage(text=str(t[1]+' ราคา :' + str(price) + '฿')))
            elif re.split('; |, |\*|\n| |/|-',incomingText)[0]  in conditionText_Sell:
                t = re.split('; |, |\*|\n| |/|-',incomingText)
                _pair = 'THB_'+t[1].upper()
                _amount = t[2]
                _rat = bitkub.get_last_price(_pair)
                price = _rat['last']
                a = ('%f' % float(_amount)).rstrip('0').rstrip('.')
                try:
                    price = t[3]
                    sellResponse = bitkub.sell(_pair,  float(a), float(price),lineOrderToken,'')
                except IndexError :
                    sellResponse = bitkub.sell(_pair,  float(a), float(price),lineOrderToken,'')
                
                
                if(sellResponse['error']==0):
                    line_bot_api.reply_message(replyToken, TextSendMessage(text='สั่งขาย '+str(t[1])+' ที่ราคา : '+str(price)+'฿ จำนวน '+str(_amount)+' สำเร็จ ไอ้สัส'))
                else:
                    line_bot_api.reply_message(replyToken, TextSendMessage(text='สั่งขาย Error : {} '.format(bitkub.errorCode[sellResponse['error']])))
            elif re.split('; |, |\*|\n| |/|-',incomingText.lower())[0]  in conditionText_BotRunCommand:
                t = re.split('; |, |\*|\n| |/|-',incomingText)
                try:
                    stopLimit = t[1]
                    botActivateDb.update_one({'Instance': APIKEYBITKUB},
                               {'$set': {'Activate': True ,'Stop_Loss_at_Money': stopLimit}
                                }
                               ,upsert=True
                               )
                    line_bot_api.reply_message(replyToken, TextSendMessage(text='สั่งรันบอทแล้วตั้ง หยุดเมื่อ ทุนเท่ากับ '+str(t[1])+'฿ สำเร็จ ไอ้สัส'))
                except IndexError :
                    botActivateDb.update_one({'Instance': APIKEYBITKUB},
                               {'$set': {'Activate': True  }
                                }
                               ,upsert=True
                               )
                    line_bot_api.reply_message(replyToken, TextSendMessage(text='สั่งรันบอทแล้วตั้ง สำเร็จ ไอ้สัส'))
                # if(sellResponse['error']==0):
                
                # else:
                    # line_bot_api.reply_message(replyToken, TextSendMessage(text='สั่งรันบอทแล้วตั้ง Error : {} '))
            elif re.split('; |, |\*|\n| |/|-',incomingText.lower())[0]  in conditionText_BotStopCommand:
                t = re.split('; |, |\*|\n| |/|-',incomingText)
                try:
                    stopLimit = t[1]
                    botActivateDb.update_one({'Instance': APIKEYBITKUB},
                               {'$set': {'Activate': True ,'Stop_Loss_at_Money': stopLimit}
                                }
                               ,upsert=False
                               )
                    line_bot_api.reply_message(replyToken, TextSendMessage(text='สั่งปิดรันบอทแล้วตั้ง หยุดเมื่อ ทุนเท่ากับ '+str(t[1])+'฿ สำเร็จ ไอ้สัส'))
                except IndexError :
                    botActivateDb.update_one({'Instance': APIKEYBITKUB},
                               {'$set': {'Activate': False  }
                                }
                               ,upsert=True
                               )
                    line_bot_api.reply_message(replyToken, TextSendMessage(text='สั่งปิดบอทแล้วตั้ง สำเร็จ ไอ้สัส'))
                # if(sellResponse['error']==0):
                
                # else:
                    # line_bot_api.reply_message(replyToken, TextSendMessage(text='สั่งรันบอทแล้วตั้ง Error : {} '))
            elif re.split('; |, |\*|\n| |/|-',incomingText)[0]  in conditionText_OrderOpen:
                t = re.split('; |, |\*|\n| |/|-',incomingText)
                # symbol = t[1].upper()
                # _pair = 'THB_'+t[1].upper()
                
                result = ''
                i=0
                bal,aData = bitkub.get_balance_assets()
                for ba in bal:
                    if(ba['symbol']=='THB' or ba['symbol']=='DON' or ba['symbol']=='LUNA2' or ba['symbol']=='TRX' ):
                        # if(ba['symbol']=='THB'):
                            # cash = ba['available']
                        pass
                    else:
                        symbol = ba['symbol']
                        _pair = 'THB_'+symbol.upper()
                        
                        aOpenOrder = bitkub.getSymOpenOrder(_pair)
                        aOpenOrderResult = aOpenOrder['result']
                        for resultOrder in aOpenOrderResult:
                            i+=1
                            _sym=symbol
                            _id=resultOrder['id']
                            _sd =resultOrder['side']
                            _hash=resultOrder['hash']
                            _rate=resultOrder['rate']
                            _amount=resultOrder['amount']
                            result += str(i) + ': '+str(_sd) + ' ' +str(_sym) +' : ราคา :' + str(_rate) + '฿ จำนวน :'+str(_amount)+' id : ' +str(_id) + ' hash : ' + str(_hash) + '\n'
                if(result is None or len(result) <=0 ):
                    result='ไม่พบ Order ที่เปิด'
                    # bitkub.cancelOpenOrder(_sym, _id, _sd,_hash,_rate,_amount,lineOrderToken)
                    # remove = profitDb[APIKEYBITKUB].delete_one({"hash":_hash})
                    # print('ยกเลิกออเดอร์ตั้งขายก่อนหน้า : ',symbol)
                # if(sellResponse['error']==0):
                line_bot_api.reply_message(replyToken, TextSendMessage(text=result))
            elif incomingText in conditionText_Wallet:
                res = bitkub.get_wallets_assets()
                if res['error'] == 0:
                    currency = res['result']
                    result = ''
                    for i in currency:
                        ccc = currency.get(i)
                        if ccc > 0 :
                            result += str(i) + ' : ' + str(ccc ) +'\n'
                line_bot_api.reply_message(replyToken, TextSendMessage(text=result))
                                           
            elif re.split('; |, |\*|\n| |/|-',incomingText)[0]  in conditionText_CancelOrder:
                t = re.split('; |, |\*|\n| |/|-',incomingText)
                _sym = t[1].upper()
                _id = t[3].upper()
                _sd = t[2].upper()
                _hash = t[4].upper()
                _rate = ' '
                _amount = ' '
                Response = bitkub.cancelOpenOrder('THB_'+_sym, _id, _sd,_hash,_rate,_amount,lineOrderToken)
                
                if(Response['error']==0):
                    line_bot_api.reply_message(replyToken, TextSendMessage(text='ยกเลิกออเดอร์ '+str(t[1])+' สำเร็จ ไอ้สัส'))
                else:
                    line_bot_api.reply_message(replyToken, TextSendMessage(text='ยกเลิกออเดอร์ Error : {} '.format(bitkub.errorCode[Response['error']])))
            else:
                line_bot_api.reply_message(replyToken, TextSendMessage(text=incomingText.split(',')[0]))
            lineLog[APIKEYBITKUB].insert_one(data)
        except LineBotApiError as e:
            print(str(e))
            line_bot_api.reply_message(replyToken, TextSendMessage(text=str(e)))
    except Exception as e:
        line_bot_api.reply_message(replyToken, TextSendMessage(text=str(e)))
        return str(e)
        
    return 'Webhooks with Python in anaconda and dev by Toeimon in Iphone Rose Gold 13'

if __name__ == '__main__':
    app.run(debug=False)
    orig_stdout = sys.stdout
    
    log_path = 'E:\\LogBot\\'
    if not os.path.exists(log_path):
        os.makedirs(log_path)
        
    f = open(log_path+'WebHook_'+str(tb_name)+'.txt', 'a')
    sys.stdout = f
    
    sys.stdout = orig_stdout
    f.close()
