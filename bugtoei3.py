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

API_HOST = 'https://api.bitkub.com'
apikey = 'APIKEY_BITKUB' 
apisecret = b'APISECRET_BITKUB'

fund = 1000
gap = 10
MyWatcher = ['ZIL']

API_KEY = apikey
API_SECRET = apisecret


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
s = sched.scheduler(time.time, time.sleep)

def json_encode(data):
    	return json.dumps(data, separators=(',', ':'), sort_keys=True)

def sign(data):
	j = json_encode(data)
	# print('Signing payload: ' + j)
	h = hmac.new(API_SECRET, msg=j.encode(), digestmod=hashlib.sha256)
	return h.hexdigest()

def getServerTime():
    response = requests.get(API_HOST + '/api/servertime')
    ts = int(response.text)
    # print('Server time: ' + response.text)
    return(ts)


def buy(_pair,_amt,_rat):
    header = {
	'Accept': 'application/json',
	'Content-Type': 'application/json',
	'X-BTK-APIKEY': API_KEY,
    }
    data = {
        'sym': _pair,
        'amt': _amt, # THB amount you want to spend
        'rat': _rat,
        'typ': 'limit',
        'ts': getServerTime(),
    }
    signature = sign(data)
    data['sig'] = signature
    
    print('Payload with signature: ' + json_encode(data))
    response = requests.post(API_HOST + '/api/market/place-bid', headers=header, data=json_encode(data))
    res = response.json()
    if(res['error']==0):
        sendLine('ซื้อเข้า :{} ที่ราคา : {:,.3f} จำนวน : {} โดนค่า Fee {:,.3f}฿'.format(_pair,_rat,_amt,res['result']['fee']))
    else:
        sendLine('ซื้อเข้า :{} ที่ราคา : {:,.3f} จำนวน : {} ผลลัพธ์ {}฿'.format(_pair,_rat,_amt,errorCode[res['error']]))

    return response

def sell(_pair,_amt,_rat):
    header = {
	'Accept': 'application/json',
	'Content-Type': 'application/json',
	'X-BTK-APIKEY': API_KEY,
    }
    data = {
        'sym': _pair,
        'amt': _amt, # THB amount you want to spend
        'rat': _rat,
        'typ': 'limit',
        'ts': getServerTime(),
    }
    signature = sign(data)
    data['sig'] = signature

    print('Payload with signature: ' + json_encode(data))

    response = requests.post(API_HOST + '/api/market/place-ask', headers=header, data=json_encode(data))
    res = response.json()
    #data = data['result']
    if(res['error']==0):
        sendLine('ขายออก :{} ที่ราคา : {:,.3f} จำนวน : {} โดนค่า Fee {:,.3f}฿'.format(_pair,_rat,_amt,res['result']['fee']))
    else:
       
        sendLine('ขายออก :{} ที่ราคา : {:,.3f} จำนวน : {} Error : {}฿'.format(_pair,_rat,_amt,errorCode[res['error']]))

    return response

def CheckCondition(sc,coin,price):
    # coin= 'THB_BTC', price = 1050000
    text = ''
    check_buy = condition[coin]['buy']
    if price <= check_buy:
        txt = '{} ราคาลงแล้ว เหลือ: {:,.3f} รีบซื้อด่วน!\n(ราคาที่อยากได้: {:,.3f})'.format(coin,price,check_buy)
        #print(txt)
        text += txt + '\n'
        sendLine(text)
        
    check_sell = condition[coin]['sell']
    if price >= check_sell:
        txt = '{} ราคาขึ้นแล้ว ล่าสุดเป็น: {:,.3f} รีบขายด่วน!\n(ราคาที่อยากขาย: {:,.3f})'.format(coin,price,check_sell)
        #print(txt)
        text += txt + '\n'
        sendLine(text)
    print('CheckCondition',coin,price)
    # s.enter(10, 1, CheckCondition, kwargs={'sc':s,'coin': coin,'price': price})
    return text


def checkBalance():
    header = {
	'Accept': 'application/json',
	'Content-Type': 'application/json',
	'X-BTK-APIKEY': API_KEY,
    }
    data = {
        'ts': getServerTime(),
    }
    signature = sign(data)
    data['sig'] = signature
    # print('Payload with signature: ' + json_encode(data))
    response = requests.post(API_HOST + '/api/market/balances', headers=header, data=json_encode(data))
    data = response.json()
    data = data['result']
    # print(response.json())
    
    return(data)

    
def sendLine(_msg):
    token = 'LINENOTIFYTOKEN'
    url = "https://notify-api.line.me/api/notify"
    headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
    r = requests.post(url, headers=headers, data = {'message':_msg})
    # print (r.text)
    
def getAllPrice():
    response = requests.get(API_HOST + '/api/market/ticker')
    result = response.json()
    return result
    
def calc(sc):
    allText = ''
    dataBalance = checkBalance()
    THB = dataBalance['THB']['available']
    THBReserve = dataBalance['THB']['reserved']
    AllMyMoney = 0
    THBinCOIN = 0
    result = getAllPrice()
    for i in dataBalance:
        if dataBalance[i]['reserved'] > 0 or dataBalance[i]['available'] > 0 :
            dataBalance[i]['symbol'] = i
    # for c in MyWatcher:
            sym = dataBalance[i]['symbol']
            currentSym = 'THB_'+sym
            if  currentSym in rebalanceTarget:
                rebalText = rebalance('THB_'+sym,sym,rebalanceTarget['THB_'+sym],True,gap)
                dataBalance = checkBalance()
                THB = dataBalance['THB']['available']
                THBReserve = dataBalance['THB']['reserved']
                result = getAllPrice()
            else:
                rebalText = 'ไม่เปิดบอท'
            
            
            
            available = dataBalance[i]['available']
            reserved = dataBalance[i]['reserved']
            try:
                data = result['THB_'+sym]
                last = data['last']
                myMoney = (reserved + available) * last
                # xx = THBinCOIN + myMoney
                THBinCOIN += myMoney
                # AllMyMoney += xx
                text = ' {} : {}\n Has : {}{} \n Order : {} {}\n THB : {:,.2f}฿ \n {} \n\n'.format(str(sym),str(last),str(available),str(sym),str(reserved),str(sym),myMoney,rebalText)
                allText += text
            except KeyError:
                continue
            
    if(THBReserve==0):
        x =(THB + THBinCOIN) - fund
    else:
        x = (THBReserve +(THB + THBinCOIN)) - fund 
    xText = '{:,.2f}฿'.format(x)
    # AllMyMoney = (THB+AllMyMoney+THBReserve )
    # sendBalanceText =' ทุนให้บอท : {}฿ \n {} : {}฿  \n เงินในเหรียญ : {:,.2f}฿ \n เงินใน Order : {:,.2f}฿ \n กำไรขาดทุน  {:,.2f}฿ \n รวม  {:,.2f}฿ \n '.format(str(fund),str('เงินสด'),str(THB),THBinCOIN,THBReserve,x,AllMyMoney) 
    # sendLine( '```'+allText+'```' + '\n ' +  '```' + sendBalanceText + '```')    
    AllMyMoney = (THB+THBinCOIN+THBReserve )
    sendBalanceText =' ทุนให้บอท : {}฿ \n {} : {}฿  \n เงินในเหรียญ : {:,.2f}฿ \n เงินใน Order : {:,.2f}฿ \n กำไรขาดทุน  {:,.2f}฿ \n รวม  {:,.2f}฿ \n '.format(str(fund),str('เงินสด'),str(THB),THBinCOIN,THBReserve,x,AllMyMoney) 
    sendLine( '```'+allText+'```' + '\n ' +  '```' + sendBalanceText + '```')    
    # sc.enter(60, 1, calc, (sc,))
def balances():
    header = {
	'Accept': 'application/json',
	'Content-Type': 'application/json',
	'X-BTK-APIKEY': API_KEY,
    }
    data = {
        'ts': getServerTime(),
    }
    signature = sign(data)
    data['sig'] = signature
    # print('Payload with signature: ' + json_encode(data))
    response = requests.post(API_HOST + '/api/market/balances', headers=header, data=json_encode(data))
    data = response.json()
    #data = data['result']
    # print(response.json())
    return(data)


def ticker(_sym):
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
    response = requests.get(API_HOST + '/api/market/ticker?sym='+_sym)
    data = response.json()
    #data = data['result']
    # print(response.json())
    return(data)
   

def rebalance(_pair , _token_name , _target,_OrderActivate,_gap):
    returnText = ''
    pair = _pair#'THB_KUB' #เหรียญ
    token_name =_token_name #'KUB' #เหรียญ

    balance_coin=balances()
    balance_coin=balance_coin['result'][token_name]['available'] + balance_coin['result'][token_name]['reserved']
    #print('จำนวนเหรียญในบัญชี' , balance_coin , 'เหรียญ')

    balance_thb=balances()
    balance_thb=balance_thb['result']['THB']['available'] + balance_thb['result']['THB']['reserved']
    #print('จำนวนเงินในบัญชี' , balance_thb , 'บาท')

    last_price = ticker(pair)
    last_price = last_price[pair]['last']
    #print('ราคาเหรียญล่าสุด' , last_price , 'บาท')

    balance_value = balance_coin*last_price
    #print('มูลค่าเหรียญ' ,  balance_value , 'บาท')

    # port = balance_thb + balance_value
    # portfolio = 'มูลค่าพอร์ต  {:,.2f}  บาท'.format(port)
    # print('มูลค่าพอร์ต' , portfolio , 'บาท')

    fix_value = _target #ใส่จำนวนเงินที่ต้องการrebalance
    amount = balance_value - fix_value
    print(balance_value , ': balance_value <> fix_value :',fix_value , ' amount :' , amount)
    if balance_value > fix_value:
        amount = balance_value - fix_value
        amountToSell = amount / last_price
        # print(amount)
        if amount > _gap: #มูลค่าเพิ่มมากกว่าเท่าไหร่ถึงจะแจ้งเตือน
            print('ขายออก' , amount , 'บาท')
            #print(type(amount))
            #messenger.sendtext('Sell ' + str(float(amount)) +' Baht')
            # sendLine('{} Sell {:,.2f} baht @ {:,.2f} '.format(_pair,amount,last_price))
            if _OrderActivate == True:
                sell(_pair,amountToSell,last_price)
            returnText =  '{} Sell {:,.2f} baht @ {:,.2f} '.format(_pair,amountToSell,last_price)
        else:
            # print('Rebalance : Waiting')
            returnText = 'Rebalance : Waiting'
        # messenger.sendtext('Rebalance : Waiting')
    elif balance_value < fix_value:
        amount = fix_value - balance_value
        # print(amount)
        if amount > _gap: #มูลค่าลดมากกว่าเท่าไหร่ถึงจะแจ้งเตือน
            print('ซื้อเข้า' , amount , 'บาท')
            # sendLine('{} Buy {:,.2f} baht @ {:,.2f} '.format(_pair,amount,last_price))
            if _OrderActivate == True:
                buy(_pair,amount,last_price)
            returnText =  '{} Buy {:,.2f} baht @ {:,.2f} '.format(_pair,amount,last_price)
        else:
            # print('Rebalance : Waiting')
            returnText = 'Rebalance : Waiting'
            #messenger.sendtext('Rebalance : Waiting')
    else:
        # print('Not yet')
        returnText = 'Not yet'
    return returnText

    
def main():
    # s.enter(1, 1,  calc, (s,))
    calc(sc=None)
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
    print('-----')
    # exit()
    
    
        # time.sleep(60)
    
    
if __name__ == "__main__":
    main()

