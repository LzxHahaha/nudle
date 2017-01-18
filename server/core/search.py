# coding=utf-8
import numpy as np

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

    # TODO: split image

    hist, features = get_feature(image, voc)
    input_feature = np.vstack((hist, features))

    # 找出
    lib_images = images.find({})
    lib_features = []
    image_names = []
    for i in lib_images:
        lib_features.append(np.append(i['hist'], i['feature'], axis=0))
        image_names.append(i['name'])
    lib_features = np.array(lib_features)

    # 将图片的 Histogram 与数据库里的相乘
    score = (np.dot(input_feature.T, lib_features.T))[0][0]
    sort = np.argsort(-score)
    result = [image_names[i] for i in sort]

    # # 如果要保存输入的话，先判断一下是否重复
    if save:
        input_score = (np.dot(input_feature.T, input_feature))[0][0]
        first_score = score[sort[0]]
        if input_score != first_score:
            save_image(image)

    # 计算距离并排序
    # TODO: 优化这段，替换掉上面的
    # lib_images = images.find({})
    # image_count = images.count()
    # distances = np.zeros(image_count)
    # images_names = []
    # for i in range(image_count):
    #     feature = np.append(lib_images[i]['hist'], lib_images[i]['feature'], axis=0)
    #     distances[i] = np.linalg.norm(input_feature - feature)
    #     images_names.append(lib_images[i]['name'])
    #
    # sort = np.argsort(distances)
    # result = [images_names[i] for i in sort]

    return result, input_feature.T.tolist()


def save_image(image):
    # TODO: 异步保存图片
    pass
