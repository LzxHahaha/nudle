# coding=utf-8
import numpy as np
import scipy.spatial

from core.feature import get_feature
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

    # TODO: split image

    hist, features = get_feature(image, voc)
    input_feature = np.vstack((hist, features))

    # 计算距离并排序
    lib_images = images.find({})
    images_names = []
    features = []
    for i in lib_images:
        feature = np.append(i['hist'], i['feature'], axis=0)
        features.append(feature)
        images_names.append(i['name'])
    features = np.array(features).T
    distances = scipy.spatial.distance.cdist(features[0].T, input_feature.T)

    sort = np.argsort(distances.T)
    result = [{'name': images_names[i], 'distance': distances[i][0]} for i in sort[0]]

    return result, (input_feature.T.tolist())[0]
