# coding=utf-8
import cv2
import numpy as np
import saliency_cut
import scipy.cluster.vq as vq
from skimage.feature import local_binary_pattern

from core.sift import sift
from core.saliency_rc_cut import cut
from utils.helper import try_load
from exceptions import *
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


class SaliencyBoF:
    def __init__(self, image):
        self.image = try_load(image)
        self.features = None
        self.cut_mask = None

    @staticmethod
    def base_hist(image, useless_area):
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        v_image = hsv_image[:, :, 2]
        # H/S Histogram
        hist_h = cv2.calcHist([hsv_image], [0], None, [64], [0, 180])
        hist_s = cv2.calcHist([hsv_image], [1], None, [16], [0, 256])
        # LBP
        lbp_image = local_binary_pattern(v_image, 8 * 3, 3)
        lbp_image = np.uint8(lbp_image)
        hist_lbp = cv2.calcHist([lbp_image], [0], None, [256], [0, 256])
        # 扣除掉没用的部分
        hist_h[0][0] -= useless_area
        hist_s[0][0] -= useless_area
        hist_lbp[-1][0] -= useless_area

        return hist_h.T[0], hist_s.T[0], hist_lbp.T[0]

    @staticmethod
    def sift_count(image, dictionary):
        dict_len = len(dictionary)
        features = np.zeros(dict_len, np.float32)
        key_points, descriptor = sift(image)
        if descriptor is None:
            return np.zeros(dict_len)
        words, distance = vq.vq(descriptor, dictionary)
        for word in words:
            features[word] += 1

        return features

    @staticmethod
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

    def get_histograms(self, dictionary):
        image = self.image.copy()

        self.cut_mask = saliency_cut.rc_mask(image)
        fg, bg, fg_area, bg_area = cut(image, self.cut_mask)
        f_h, f_s, f_lbp = self.base_hist(fg, bg_area)
        if bg is None:
            b_h = np.zeros(64)
            b_s = np.zeros(16)
            b_lbp = np.zeros(256)
        else:
            b_h, b_s, b_lbp = self.base_hist(bg, fg_area)
        sift_hist = self.sift_count(fg, dictionary)

        self.features = (f_h, f_s, f_lbp, sift_hist, b_h, b_s, b_lbp)
        return self.features

    def compare_hist(self, other):
        distance = 0
        for i in [0, 1, 3, 4, 5]:
            distance += chi_square(self.features[i], other[i])
        distance += 3 * chi_square(self.features[2], other[2])
        distance += 2 * chi_square(self.features[6], other[6])
        return distance


def chi_square(h1, h2):
    result = cv2.compareHist(h1, h2, cv2.HISTCMP_CHISQR_ALT) / 2
    return (result - np.mean(h1)) / np.std(h1)
