# coding=utf-8
import cv2
import numpy as np
import scipy.cluster.vq as vq
from skimage.feature import local_binary_pattern

from core.sift import sift
from utils.cv2helper import try_load


def get_feature(img, dictionary, lbp_weight=1):
    image = try_load(img)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    features = np.zeros((len(dictionary), 1), np.uint)

    # H/S Histogram
    hist_h = cv2.calcHist([hsv_image], [0], None, [64], [0, 180])
    hist_s = cv2.calcHist([hsv_image], [1], None, [16], [0, 256])
    # LBP
    lbp_image = local_binary_pattern(gray_image, 8 * 3, 3)
    lbp_image = np.float32(lbp_image)
    hist_v = cv2.calcHist([lbp_image], [0], None, [256], [0, 256])
    # LBP 权重
    if lbp_weight > 1:
        hist_v *= lbp_weight

    # 词频统计
    key_points, descriptor = sift(image)
    words, distance = vq.vq(descriptor, dictionary)
    for word in words:
        features[word][0] += 1

    return np.vstack((hist_h, hist_s, hist_v)), features
