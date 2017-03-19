# coding=utf-8
import cv2
import numpy as np
import saliency_cut
import scipy.cluster.vq as vq
from skimage.feature import local_binary_pattern

from core.sift import sift
from core.saliency_rc_cut import cut
from utils.helper import try_load

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
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # H/S Histogram
        hist_h = cv2.calcHist([hsv_image], [0], None, [64], [0, 180])
        hist_s = cv2.calcHist([hsv_image], [1], None, [16], [0, 256])
        # LBP
        lbp_image = local_binary_pattern(gray_image, 8 * 3, 3)
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
            distance += cv2.compareHist(self.features[i], other[i], cv2.HISTCMP_CHISQR_ALT)
        distance += 3 * cv2.compareHist(self.features[2], other[2], cv2.HISTCMP_CHISQR_ALT)
        distance += 2 * cv2.compareHist(self.features[6], other[6], cv2.HISTCMP_CHISQR_ALT)
        return distance
