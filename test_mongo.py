# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 10:26:25 2022

@author: pascharapun.j
"""



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

# collection.remove({"date": {"$gt": "2012-12-15"}})

APIKEYBITKUB='APIKEY_BITKUB'
bitkub = BugKib(_apiKey=APIKEYBITKUB,_apisecret = b'APISECRET_BITKUB')
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
lineOrderToken = 'LINENOTIFYTOKEN'
# lineSignalToken = 'LINENOTIFYTOKEN'
lineSignalToken = 'LINENOTIFYTOKEN'

remove = profitDb[APIKEYBITKUB].delete_one({"hash":"TESTfwQ6dnQdC948tPHsr6De8ZazFvT"})