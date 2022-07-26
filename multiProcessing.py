from __future__ import print_function
import time

def job(a,x):
    for i in range(5):
        x += 1
        time.sleep(0.5)
        print('%s=%d'%(a,x))



import multiprocessing as mp

params = [0.5]

def function(name, params):
    print('sleeping for', name)
    time.sleep(params[0])
    return time.time()

names = list('onecharnamEs')
tradeOption = {
                'GT':{'Buy':50,'Sell':295,'MaxAmt':300,'firstInitial':0,'timeframe':'5','profitTotake':10,'tradeStyle':'fixProfit'},
                'MANA':{'Buy':50,'Sell':295,'MaxAmt':300,'firstInitial':0,'timeframe':'5','profitTotake':10,'tradeStyle':'fixProfit'},
                'BNB':{'Buy':100,'Sell':594,'MaxAmt':600,'firstInitial':0,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
                'ALPHA':{'Buy':50,'Sell':295,'MaxAmt':300,'firstInitial':0,'timeframe':'5','profitTotake':10,'tradeStyle':'fixProfit'},
                'SOL':{'Buy':50,'Sell':195,'MaxAmt':200,'firstInitial':0,'timeframe':'5','profitTotake':10,'tradeStyle':'fixProfit'},
                'GALA':{'Buy':50,'Sell':195,'MaxAmt':200,'firstInitial':0,'timeframe':'5','profitTotake':10,'tradeStyle':'fixProfit'},
                'SUSHI':{'Buy':50,'Sell':195,'MaxAmt':200,'firstInitial':0,'timeframe':'5','profitTotake':'10','tradeStyle':'fixProfit'},
                'BTC':{'Buy':100,'Sell':495,'MaxAmt':500,'firstInitial':0,'timeframe':'5','profitTotake':10,'tradeStyle':'stepProfit'},
                }

if(__name__=='__main__'):
    p1 = mp.Process(target=job,args=('x',1))
    p2 = mp.Process(target=job,args=('y',11))
    p1.start()
    p2.start()
    print('สั่งงานไปแล้ว')