# coding=utf-8
import argparse
import numpy as np
import scipy.cluster.vq as vq
import glob
import time
import sys
from multiprocessing import Pool

import utils.mongo as mongo
from core.sift import sift

TRAIN_SEGMENT = 100


def get_features(offset, end):
    kp, result = sift(image_paths[offset])
    print '\r%d/%d' % (offset + 1, train_count),
    for i in range(offset + 1, end):
        kp, d = sift(image_paths[i])
        result = np.vstack((result, d))
        print '\r%d/%d' % (i + 1, train_count),
    return result

if __name__ == '__main__':
    # 配置脚本参数
    parser = argparse.ArgumentParser()
    parser.add_argument('-l, --lib', action='store', dest='library', help='Image library\'s name.')
    # 读取参数
    params = parser.parse_args()
    lib = params.library

    # 检查之前是否已经生成过
    db = mongo.get_db()
    dictionaries = db.dictionaries
    old_lib = dictionaries.find_one({'library': lib})
    if old_lib is not None:
        while 1:
            confirm = raw_input('Already have dictionary of library [%s], '
                                'sure you want to overwrite it? [y/n]: ' % lib)
            if confirm.lower() == 'y':
                break
            elif confirm.lower() == 'n':
                sys.exit()

    # 取 1/8 的图片生成做训练
    print 'Start get SIFT feature from images...'
    start_time = time.time()
    image_paths = glob.glob('./static/%s/*' % lib)
    path_count = len(image_paths)
    train_count = path_count // 8
    offset = 1
    key_points, descriptors = sift(image_paths[0])
    print '%d/%d' % (1, train_count),
    tmp = train_count

    if tmp > TRAIN_SEGMENT:
        res = get_features(offset, TRAIN_SEGMENT)
        descriptors = np.vstack((descriptors, res))
        tmp -= TRAIN_SEGMENT
        offset += TRAIN_SEGMENT
    res = get_features(offset, train_count)
    descriptors = np.vstack((descriptors, res))

    print '\nDone. Use %fs.' % (time.time() - start_time)

    # k-means 聚合
    print 'Start cluster...'
    start_time = time.time()
    cookbook, variance = vq.kmeans(descriptors, 100, 10)
    print 'Done. Use %fs.\n' % (time.time() - start_time)

    # 保存数据到数据库
    print 'Save cookbook to database...\n'
    dictionaries.update_one({'library': lib}, {'$set': {'dictionary': cookbook.tolist()}}, True)
    print 'All done.'
