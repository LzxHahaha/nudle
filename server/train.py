# coding=utf-8
import argparse
import numpy as np
import scipy.cluster.vq as vq
import glob
import time
import sys
import os
from multiprocessing import Pool

import utils.mongo as mongo
from core.sift import sift

TRAIN_SEGMENT = 100


def get_features(paths):
    print '[%s]\tProcessing...' % os.getpid()
    kp, res = sift(paths[0])
    for i in paths[1:]:
        kp, d = sift(i)
        res = np.vstack((res, d))
    print '[%s]\tProcess done.' % os.getpid()
    return res

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


    def main():
        # 取 1/8 的图片生成做训练
        print 'Start get SIFT feature from images...'
        start_time = time.time()
        image_paths = glob.glob('./static/%s/*' % lib)
        path_count = len(image_paths)
        train_count = path_count // 8
        offset = 1
        key_points, descriptors = sift(image_paths[0])

        tmp = train_count
        args = []
        while tmp > TRAIN_SEGMENT:
            args.append(image_paths[offset: offset + TRAIN_SEGMENT])
            tmp -= TRAIN_SEGMENT
            offset += TRAIN_SEGMENT
        args.append(image_paths[offset: train_count])
        pool = Pool()
        result = pool.map(get_features, args)
        pool.close()
        pool.join()
        for i in result:
            descriptors = np.vstack((descriptors, i))

        print '\nDone. Use %fs.\n' % (time.time() - start_time)

        # k-means 聚合
        print 'Start cluster...'
        start_time = time.time()
        cookbook, variance = vq.kmeans(descriptors, 100, 10)
        print 'Done. Use %fs.\n' % (time.time() - start_time)

        # 保存数据到数据库
        print 'Save cookbook to database...\n'
        dictionaries.update_one({'library': lib}, {'$set': {'dictionary': cookbook.tolist()}}, True)
        print 'All done.'

    main()
