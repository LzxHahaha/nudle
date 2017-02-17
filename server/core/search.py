# coding=utf-8
import numpy as np
import scipy

from core.feature import get_feature
from utils.mongo import get_db


# TODO: 考虑保存字典到内存中
# DICTIONARIES = {}


def search(image, library, save=False):
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

    input_feature = get_feature(image, voc)

    # 计算距离并排序
    lib_images = images.find({})
    images_names = []
    features = []
    for i in lib_images:
        features.append(i['feature'])
        images_names.append(i['name'])
    features = np.array(features).T
    distances = scipy.spatial.distance.cdist(features[0].T, input_feature.T)

    sort = np.argsort(distances.T)
    result = [{'name': images_names[i], 'distance': distances[i][0]} for i in sort[0]]

    if save and distances[sort[0]] > 0:
        save_image(image)

    return result, (input_feature.T.tolist())[0]


def save_image(image):
    # TODO: 异步保存图片
    pass
