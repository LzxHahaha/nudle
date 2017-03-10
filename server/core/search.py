# coding=utf-8
import numpy as np
import cv2

from core.feature import get_histograms, concat_histogram
from utils.mongo import get_db

HIST_NAMES = [
    'foreground-h',
    'foreground-s',
    'foreground-lbp',
    'sift-statistics',
    'background-h',
    'background-s',
    'background-lbp'
]


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
    input_feature = np.float32(concat_histogram(input_hist))

    # 计算距离并排序
    lib_images = images.find({})
    images_names = []
    features = []
    for i in lib_images:
        features.append(i['feature'])
        images_names.append(i['name'])
    features = np.array(features, np.float32)
    distances = []
    for f in features:
        d = cv2.compareHist(input_feature, f, cv2.cv.CV_COMP_CHISQR)
        distances.append(d)

    sort = np.argsort(np.array(distances))
    result = [{'name': images_names[sort[i]], 'distance': distances[sort[i]]} for i in range(size)]

    histograms = {}
    for i in range(len(HIST_NAMES)):
        histograms[HIST_NAMES[i]] = input_hist[i].T[0].tolist()

    return result, histograms
