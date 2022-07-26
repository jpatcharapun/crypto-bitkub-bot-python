# -*- coding: utf-8 -*-


# import websocket

from apibutkib import BugKib
from pymongo import MongoClient
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("E:\LogBot\debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)


bitkubToei = BugKib(_apiKey='APIKEY_BITKUB' ,_apisecret = b'APISECRET_BITKUB')
client = MongoClient('mongodbAddress',27017)
db = client.bitkub
APIKEYBITKUB='APIKEY_BITKUB'
bitkubTa = BugKib(_apiKey='APIKEY_BITKUB',_apisecret = b'APISECRET_BITKUB')
# allMoney = bitkubToei.getMyMoney()
# excludeEmergency = {'LUNA','LUNA2'}
# excludeProfit = {'LUNA','KUB','DOGE','ZIL','XLM'}
# lineOrderToken = 'LINENOTIFYTOKEN'
# lineSignalToken = 'LINENOTIFYTOKEN'

botActivateDb = db.botactivate
# # botActivateDb.update_one({'Instance': APIKEYBITKUB},
# #            {'$set': {'Activate': False}
# #             }
# #            ,upsert=True
# #            )
try:
    botActivate = { "Instance": APIKEYBITKUB }
    botActivateDoc = botActivateDb.find_one(botActivate)
    if(botActivateDoc['Activate']==False):
        logSave   = {
                "CASH": "bitkub.getMyMoney()",
                "Asset": "BOT IS DEACTIVATE",
                "Signal": "BOT IS DEACTIVATE",
                "StochRSI": "BOT IS DEACTIVATE",
                "AssetInTHB":"BOT IS DEACTIVATE",
                "AvgBuyPrice":"BOT IS DEACTIVATE",
                "CurrentPrice":"BOT IS DEACTIVATE",
                "Available":"BOT IS DEACTIVATE",
                "Reserved":"BOT IS DEACTIVATE",
                "Profit":"BOT IS DEACTIVATE",
                "ProfitGoal":"BOT IS DEACTIVATE",
                # "LastUpdate": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
        # joblogDb[APIKEYBITKUB].insert_one(logSave)
        botActivateDb.update_one({'Instance': APIKEYBITKUB},
                   {'$set': {'Activate': False}
                    }
                   ,upsert=True
                   )
        # bitkub.sendLine('Stop Loss No Bot DeActivaed',token=lineOrderToken)
        abc = 'EXITED'
        sys.exit("BOT IS DEACTIVATE")
        
except Exception as e:
    abc= 'except : '+ str(e)
    pass

adf = 'Running'
# botActivate = { "Instance": APIKEYBITKUB }
# botActivateDoc = botActivateDb.find_one(botActivate)
# a = botActivateDoc['Activate']



# # bitkub.emergencySell(excludeEmergency, lineOrderToken)
# TaMoney = bitkubTa.getMyMoney()
# ToeiMoney = bitkubToei.getMyMoney()