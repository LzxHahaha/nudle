# coding=utf-8
import numpy as np

from core.feature import get_feature
from utils.mongo import get_db


# TODO: 考虑保存字典到内存中
# DICTIONARIES = {}


def search(image, library, save=False):
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
    image_feature = np.vstack((hist, features))

    # 找出
    lib_images = images.find({})
    lib_features = []
    image_names = []
    for i in lib_images:
        lib_features.append(np.append(i['hist'], i['feature'], axis=0))
        image_names.append(i['name'])
    lib_features = np.array(lib_features)

    # 将图片的 Histogram 与数据库里的相乘
    score = (np.dot(image_feature.T, lib_features.T))[0][0]
    sort = np.argsort(-score)
    result = [image_names[i] for i in sort]

    # 如果要保存输入的话，先判断一下是否重复
    if save:
        input_score = (np.dot(image_feature.T, image_feature))[0][0]
        first_score = score[sort[0]]
        if input_score != first_score:
            save = False

    return result, save
