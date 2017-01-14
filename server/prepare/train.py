# coding=utf-8
import argparse
import numpy as np
import scipy.cluster.vq as vq
import glob
import time
import sys

import utils.mongo as mongo
from core.sift import sift


# 配置脚本参数
parser = argparse.ArgumentParser()
parser.add_argument('-l', action='store', dest='library', help='Image library\'s name.')
parser.add_argument('--library', action='store', dest='library', help='Image library\'s name.')
# 读取参数
params = parser.parse_args()
lib = params.library

# 检查之前是否已经生成过
db = mongo.get_db()
dictionaries = db.dictionaries
old_lib = dictionaries.find_one({'library': lib})
if old_lib is not None:
    confirm = raw_input('Already have dictionary for library [%s], sure you want to overwrite it? [y/n]: ' % lib)
    # 只在输入 y 或者 Y 的时候继续，其他情况都终止
    if confirm.lower() == 'y':
        pass
    else:
        sys.exit()

# 取 1/8 的图片生成做训练
print 'Start get SIFT feature from images...'
image_paths = glob.glob('./%s/*' % lib)
path_count = len(image_paths)
train_count = path_count // 7
key_points, desc = sift(image_paths[0])
descriptors = desc
print '%d/%d' % (1, train_count),
for i in range(1, train_count):
    key_points, desc = sift(image_paths[i])
    descriptors = np.vstack((descriptors, desc))
    print '\r%d/%d' % (i + 1, train_count),
print '\nDone.\n'

# k-means 聚合
print 'Start cluster...'
start_time = time.time()
cookbook, variance = vq.kmeans(descriptors, 100, 10)
use_time = time.time() - start_time
print 'Done. Use %fs.\n' % use_time

# 保存数据到数据库
print 'Save cookbook to database...\n'
dictionaries.update_one({'library': lib}, {'$set': {'dictionary': cookbook.tolist()}}, True)
print 'All done.'
