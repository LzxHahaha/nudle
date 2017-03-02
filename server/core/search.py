# coding=utf-8
import numpy as np
import cv2

from core.feature import get_histograms, concat_histogram
from utils.mongo import get_db


def search(image, library):
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
    result = [{'name': images_names[i], 'distance': distances[i]} for i in sort]

    return result, {
        'foreground-h': input_hist[0].T[0].tolist(),
        'foreground-s': input_hist[1].T[0].tolist(),
        'foreground-lbp': input_hist[2].T[0].tolist(),
        'sift-statistics': input_hist[3].T[0].tolist(),
        'background-h': input_hist[4].T[0].tolist(),
        'background-s': input_hist[5].T[0].tolist(),
        'background-lbp': input_hist[6].T[0].tolist()
    }
