# coding=utf-8
import argparse
import os
import time
from multiprocessing import Manager, Pool

import utils.mongo as mongo
from utils.format_print import datetime_print
from core.feature import get_feature

SEGMENT_STEP = 100


def record(paths, lib_dict, lib_name):
    print '(%s)\tProcessing...' % os.getpid()
    doc = mongo.get_db()['images_' + lib_name]
    data = []
    for (full_path, name) in paths:
        hist, feature = get_feature(full_path, lib_dict)
        data.append({'name': name, 'hist': hist.tolist(), 'feature': feature.tolist()})
    doc.insert_many(data)
    print '(%s)\tProcess done.' % os.getpid()


if __name__ == '__main__':
    # 配置参数
    parser = argparse.ArgumentParser()
    parser.add_argument('-l, --lib', action='store', dest='library', required=True, help='Image library\'s name.')
    # 读取参数
    params = parser.parse_args()
    lib = params.library

    # 多进程Manager
    process_manager = Manager()

    # 连接数据库
    db = mongo.get_db()
    dictionaries = db.dictionaries
    dictionary = dictionaries.find_one({'library': lib})
    voc = dictionary['dictionary']
    voc = process_manager.list(voc)

    collection = 'images_' + lib
    images = db[collection]

    datetime_print('Start...')
    start = time.time()
    dir_path = '%s/static/%s' % (os.getcwd(), lib)

    image_names = []
    for path in os.walk(dir_path):
        root, dirs, files = path
        for filename in files:
            image_names.append(('%s%s/%s' % (root, dirs and '/' + dirs or '', filename), filename))
            
    args = [image_names[x:x+SEGMENT_STEP] for x in range(0, len(image_names), SEGMENT_STEP)]

    pool = Pool()
    for arg in args:
        pool.apply_async(record, args=(arg, voc, lib))
    pool.close()
    pool.join()

    print '\n'
    datetime_print('Done. Use %fs.' % (time.time() - start))

