# coding=utf-8
import numpy as np

from core.feature import get_histograms, HIST_NAMES, compare_hist
from utils.mongo import get_db


def search(image, library, size=20):
    if image is None:
        raise Exception('Image can not be None.')

    # 准备数据库
    db = get_db()
    dictionaries = db.dictionaries
    dictionary = dictionaries.find_one({'library': library})
    if dictionary is None:
        raise Exception('No library named %s.' % library)
    voc = np.array(dictionary['dictionary'])

    collection = 'images_' + library
    images = db[collection]

    input_hist = get_histograms(image, voc)

    # 计算距离并排序
    lib_images = images.find({})
    images_names = []
    features = []
    for i in lib_images:
        features.append(i['feature'])
        images_names.append(i['name'])
    distances = []
    for f in features:
        lib_feature = [np.array(x, np.float32) for x in f]
        d = compare_hist(input_hist, lib_feature)
        distances.append(d)

    sort = np.argsort(np.array(distances))
    result = [{'name': images_names[sort[i]], 'distance': distances[sort[i]]} for i in range(size)]

    histograms = {}
    for i in range(len(HIST_NAMES)):
        histograms[HIST_NAMES[i]] = input_hist[i].tolist()

    return result, histograms
