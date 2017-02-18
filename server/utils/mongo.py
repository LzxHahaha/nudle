# coding=utf-8
from pymongo import MongoClient

from config import MONGO_DB

mongo_client = MongoClient(MONGO_DB['host'], MONGO_DB['port'], connect=False)


def get_db():
    return mongo_client[MONGO_DB['db_name']]
