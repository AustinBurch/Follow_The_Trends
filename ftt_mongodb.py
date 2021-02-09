from typing import Collection
from pymongo import MongoClient
import config

client = MongoClient()

client = MongoClient("mongodb+srv://" + config.mongodb_user + ":" + config.mongodb_psswd + "@cluster0.y1xqg.mongodb.net/ftt_db?retryWrites=true&w=majority")
db = client.ftt_db

collection = db['stock_tickers']
