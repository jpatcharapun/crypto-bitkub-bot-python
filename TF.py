
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
bitkub = BugKib(_apiKey='APIKEY_BITKUB' ,_apisecret = b'APISECRET_BITKUB')


assets = bitkub.get_assets()
bal = bitkub.get_balance_assets()
aUrl = {}
aDataframe = {}
for ba in bal:
    if(ba['symbol']=='THB' or ba['symbol']=='DON'):
        if(ba['symbol']=='THB'):
            cash = ba['available']
        pass
    else:
        
        symbol = ba['symbol']

        lastBuyPrice = 0
        MyDataFrame ,aUrl[symbol]  = bitkub.get_candle(symbol, timeframe='5')
        aDataframe[symbol] = MyDataFrame