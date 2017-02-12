# coding=utf-8
from pymongo import MongoClient

# TODO: read from config file
mongo_config = {
    'host': 'localhost',
    'port': 27017,
    'db_name': 'image-retrieval'
}

mongo_client = MongoClient(mongo_config['host'], mongo_config['port'], connect=False)


def get_db():
    return mongo_client[mongo_config['db_name']]
