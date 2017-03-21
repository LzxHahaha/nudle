# coding=utf-8
import numpy as np

from core.SaliencyaBoF import SaliencyBoF, HIST_NAMES
from exceptions import *
from utils.mongo import get_db


def search(image, library, size=20):
    if image is None:
        raise UnknownImageError('None')

    # 准备数据库
    db = get_db()
    dictionaries = db.dictionaries
    dictionary = dictionaries.find_one({'library': library})
    if dictionary is None:
        raise UnknownLibraryError(library)
    voc = np.array(dictionary['dictionary'])

    collection = 'images_' + library
    images = db[collection]

    sbf = SaliencyBoF(image)
    sbf.get_histograms(voc)

    # 计算距离并排序
    lib_images = images.find({}, {'name': 1, 'feature': 1, '_id': 0})
    images_names = []
    distances = []
    for i in lib_images:
        images_names.append(i['name'])
        d = sbf.compare_hist([np.array(h, np.float32) for h in i['feature']])
        distances.append(d)

    sort = np.argsort(np.array(distances))[:size]
    result = [{'name': images_names[i], 'distance': distances[i]} for i in sort]

    histograms = {}
    for i in range(len(HIST_NAMES)):
        histograms[HIST_NAMES[i]] = sbf.features[i].tolist()

    return result, histograms, sbf.cut_mask
