# coding=utf-8
import argparse
import os
import time

import utils.mongo as mongo
from utils.format_print import datetime_print
from core.feature import get_feature


# 配置参数
parser = argparse.ArgumentParser()
parser.add_argument('-l, --lib', action='store', dest='library', required=True, help='Image library\'s name.')
# 读取参数
params = parser.parse_args()
lib = params.library


# 连接数据库
db = mongo.get_db()
dictionaries = db.dictionaries
dictionary = dictionaries.find_one({'library': lib})
voc = dictionary['dictionary']

collection = 'images_' + lib
images = db[collection]

datetime_print('Start...')
start = time.time()
dir_path = '%s/static/%s' % (os.getcwd(), lib)

for path in os.walk(dir_path):
    root, dirs, files = path
    image_count = len(files)
    for i in range(image_count):
        print '\r%d/%d' % (i + 1, image_count),
        hist, features = get_feature('%s/%s' % (root, files[i]), voc)
        images.insert({'name': files[i], 'hist': hist.tolist(), 'feature': features.tolist()})
print '\n'
datetime_print('Done. Use %fs.' % (time.time() - start))
