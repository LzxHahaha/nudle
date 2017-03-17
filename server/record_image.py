# coding=utf-8
import cv2
import argparse
import os
import time
import traceback
from multiprocessing import Manager, Pool, cpu_count

import utils.mongo as mongo
from utils.format_print import datetime_print
from utils.helper import to_jpg
from core.feature import get_histograms


def record(paths, lib_dict, lib_name):
    process_start = time.time()
    print('(%s)\tProcessing: %d tasks' % (os.getpid(), len(paths)))
    doc = mongo.get_db()['images_' + lib_name]
    data = []
    for (full_path, name) in paths:
        try:
            image = cv2.imread(full_path)
            image = to_jpg(image)
            histograms = get_histograms(image, lib_dict)
            histograms = [i.tolist() for i in histograms]
            data.append({'name': name, 'feature': histograms})
        except Exception:
            print('(%s)\t[%s]\n%s' % (os.getpid(), full_path, traceback.format_exc()))
    doc.insert_many(data)
    print('(%s)\tProcess done. -- %fs --' % (os.getpid(), time.time() - process_start))


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

