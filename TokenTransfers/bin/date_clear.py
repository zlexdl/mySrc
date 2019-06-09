
import datetime
from pymongo import MongoClient

conn = MongoClient('192.168.1.8', 27017)

# 前一小时
now = datetime.datetime.now()
d1 = now - datetime.timedelta(hours=1)

db = conn.explorerdb_btc_es

addresses = db.addresses
txes = db.txes
addresses.delete_many({'update_dt': {'$lt': d1.timestamp()}})
txes.delete_many({'update_dt': {'$lt': d1.timestamp()}})


db = conn.explorerdb_btc
addresses = db.addresses
txes = db.txes
addresses.delete_many({'update_dt': {'$lt': d1.timestamp()}})
txes.delete_many({'update_dt': {'$lt': d1.timestamp()}})