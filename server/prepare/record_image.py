# coding=utf-8
import argparse
import os
import time

import utils.mongo as mongo
from core.feature import get_feature


# 配置参数
parser = argparse.ArgumentParser()
parser.add_argument('-l', action='store', dest='library')
parser.add_argument('--library', action='store', dest='library')
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

print 'Start get feature from images...'
start = time.time()

for path in os.walk('%s/%s' % (os.getcwd(), lib)):
    root, dirs, files = path
    image_count = len(files)
    for i in range(image_count):
        print '\r%d/%d' % (i + 1, image_count),
        hist, features = get_feature('%s/%s' % (root, files[i]), voc)
        images.insert({'name': files[i], 'hist': hist.tolist(), 'feature': features.tolist()})
print '\nDone. Use %fs.\n' % (time.time() - start)
