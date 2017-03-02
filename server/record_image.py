# coding=utf-8
import argparse
import os
import time
from multiprocessing import Manager, Pool, cpu_count

import utils.mongo as mongo
from utils.format_print import datetime_print
from core.feature import get_histograms, concat_histogram


def record(paths, lib_dict, lib_name):
    print '(%s)\tProcessing: %d tasks' % (os.getpid(), len(paths))
    doc = mongo.get_db()['images_' + lib_name]
    data = []
    process_start = time.time()
    for (full_path, name) in paths:
        histograms = get_histograms(full_path, lib_dict)
        histograms = concat_histogram(histograms)
        data.append({'name': name, 'feature': histograms.tolist()})
    doc.insert_many(data)
    print '(%s)\tProcess done. -- %fs --' % (os.getpid(), time.time() - process_start)


if __name__ == '__main__':
    datetime_print('Starting...')
    # 配置参数
    parser = argparse.ArgumentParser()
    parser.add_argument('-l, --lib', action='store', dest='library', required=True, help='Image library\'s name.')
    # 读取参数
    params = parser.parse_args()
    lib = params.library

    # 多进程Manager
    process_manager = Manager()

    datetime_print('Connecting to database...')
    # 连接数据库
    db = mongo.get_db()
    dictionaries = db.dictionaries
    dictionary = dictionaries.find_one({'library': lib})
    voc = dictionary['dictionary']
    voc = process_manager.list(voc)

    datetime_print('Recording...')
    start = time.time()
    dir_path = '%s/static/lib_%s' % (os.getcwd(), lib)

    image_names = []
    for path in os.walk(dir_path):
        root, dirs, files = path
        for filename in files:
            image_names.append(('%s/%s' % (root, filename), filename))

    image_count = len(image_names)
    segment_count = image_count // cpu_count()
    args = [image_names[x:x + segment_count] for x in range(0, image_count, segment_count)]

    pool = Pool()
    for arg in args:
        pool.apply_async(record, args=(arg, voc, lib))
    pool.close()
    pool.join()

    datetime_print('Done. Use %fs.' % (time.time() - start))

