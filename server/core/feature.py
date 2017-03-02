# coding=utf-8
import cv2
import numpy as np
import scipy.cluster.vq as vq
from skimage.feature import local_binary_pattern

from core.sift import sift
from core.saliency_cut import cut
from utils.cv2helper import try_load


def get_histograms(img, dictionary):
    image = try_load(img)

    fg, bg, fg_area, bg_area = cut(image)
    f_h, f_s, f_lbp = base_hist(fg, lbp_weight=3, useless_area=bg_area)
    b_h, b_s, b_lbp = base_hist(bg, lbp_weight=2, useless_area=fg_area)
    sift_hist = sift_count(fg, dictionary)

    return f_h, f_s, f_lbp, sift_hist, b_h, b_s, b_lbp


def concat_histogram(histograms):
    return np.vstack(histograms).T[0]


def base_hist(image, lbp_weight=1, useless_area=0):
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
    # LBP 权重
    if lbp_weight > 1:
        hist_lbp *= lbp_weight

    return hist_h, hist_s, hist_lbp


def sift_count(image, dictionary):
    features = np.zeros((len(dictionary), 1), np.uint)
    key_points, descriptor = sift(image)
    words, distance = vq.vq(descriptor, dictionary)
    for word in words:
        features[word][0] += 1

    return features
