# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 09:35:14 2022

@author: pascharapun.j
"""
import pymongo
from bson.son import SON
import pprint
from pymongo import MongoClient
APIKEYBITKUB='APIKEY_BITKUB'
myclient = pymongo.MongoClient("mongodb://mongodbAddress/")
# db = client.bitkub
mydb = myclient["bitkub"]
mycol = mydb["profitDb."+APIKEYBITKUB]


pipeline = [
    {"$unwind": "$asset"},
    {"$group": {"_id":"$asset", "BotProfitSummary": {"$sum": "$Profit"}}},
    {"$sort": SON([("Profit", -1), ("_id", -1)])}
]

##myquery = { "asset": "BTC" ,"$sum":"$STOCHRSIk"}
##
##mydoc = mycol.find(myquery)
a = list(mycol.aggregate(pipeline))

