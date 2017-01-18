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

    # 计算距离并排序
    # TODO: 优化
    lib_images = images.find({})
    image_count = images.count()
    distances = np.zeros(image_count)
    images_names = []
    for i in range(image_count):
        feature = np.append(lib_images[i]['hist'], lib_images[i]['feature'], axis=0)
        distances[i] = np.linalg.norm(input_feature - feature)
        images_names.append(lib_images[i]['name'])

    sort = np.argsort(distances)
    result = [images_names[i] for i in sort]

    if save and distances[sort[0]] > 0:
        save_image(image)

    return result, (input_feature.T.tolist())[0]


def save_image(image):
    # TODO: 异步保存图片
    pass
