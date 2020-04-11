from pymongo import MongoClient
from random import choice

conn = MongoClient('mongodb://localhost:27017/')

db = conn.talks


def query(text):
    ret = db.raw.find({'desc': {'$regex': text}}, {'desc': 1})
    ret = list(ret)
    if ret:
        return choice(ret).get('desc')
