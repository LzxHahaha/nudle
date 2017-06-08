# coding=utf-8
import argparse
import numpy as np
import scipy.cluster.vq as vq
import glob
import time
import sys
import os
from multiprocessing import Pool, cpu_count
import pymongo

import utils.mongo as mongo
from core.sift import sift
from utils.format_print import datetime_print


def get_features(paths):
    print('(%s)\tProcessing...' % os.getpid())
    kp, res = sift(paths[0])
    for i in paths[1:]:
        kp, d = sift(i)
        res = np.vstack((res, d))
    print('(%s)\tProcess done.' % os.getpid())
    return res


def read_images(lib_name, train_step):
    image_paths = glob.glob('./static/lib_%s/*' % lib_name)
    path_count = len(image_paths)
    train_count = path_count // 8
    train_image = [image_paths[x] for x in range(0, train_count * train_step, train_step)]
    key_points, lib_descriptors = sift(image_paths[0])

    # 分段处理
    train_segment = train_count // cpu_count()
    args = [train_image[x:x + train_segment] for x in range(0, train_count, train_segment)]

    # 开多进程
    pool = Pool()
    result = pool.map(get_features, args)
    pool.close()
    pool.join()
    for i in result:
        lib_descriptors = np.vstack((lib_descriptors, i))
    return lib_descriptors

if __name__ == '__main__':
    # 配置脚本参数
    parser = argparse.ArgumentParser()
    parser.add_argument('-l, --lib', action='store', dest='library', required=True, help='Image library\'s name.')
    parser.add_argument('-s, --step', action='store', dest='step', default=1, help='Train image selected step.')
    # 读取参数
    params = parser.parse_args()
    lib = params.library
    step = int(params.step)
    if step <= 0:
        step = 1
    elif step > 8:
        step = 8

    # 检查之前是否已经生成过
    db = mongo.get_db()
    dictionaries = db.dictionaries
    old_lib = dictionaries.find_one({'library': lib})
    if old_lib is not None:
        while 1:
            confirm = input('Already have dictionary of library [%s], sure you want to overwrite it? [y/n]: ' % lib)
            if confirm.lower() == 'y':
                break
            elif confirm.lower() == 'n':
                sys.exit()

    # 取 1/8 的图片生成做训练
    datetime_print('Start get SIFT feature from images...')
    start_time = time.time()
    descriptors = read_images(lib, step)
    end_time = time.time() - start_time
    datetime_print('Done. Use %fs.\n' % end_time)

    # k-means 聚合
    datetime_print('Start cluster...')
    start_time = time.time()
    cookbook, variance = vq.kmeans(descriptors, 100, 10)
    end_time = time.time() - start_time
    datetime_print('Done. Use %fs.\n' % end_time)

    # 保存数据到数据库
    datetime_print('Save cookbook to database and try to create index...\n')
    dictionaries.update_one({'library': lib}, {'$set': {'dictionary': cookbook.tolist()}}, True)
    dictionaries.create_index([('library', pymongo.ASCENDING)], unique=True, background=True)
    datetime_print('All done.')
