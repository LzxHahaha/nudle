# coding=utf-8
import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.feature import local_binary_pattern

from core.feature import base_hist, sift_count, HIST_NAMES
from core.saliency_cut import cut
from core.sift import sift
from exceptions import *
from utils.helper import try_load
from utils.mongo import get_db


def test(img_path, dict_name):
    image = try_load(img_path)

    # 显示前景+背景切割后的SIFT特征点
    print('RC cut...')
    f, b, f_area, b_area = cut(image)
    kp_f, desc_f = sift(f)
    fg_sift = f.copy()
    cv2.drawKeypoints(f, kp_f, fg_sift, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imshow('foreground-sift', fg_sift)
    cv2.imshow('background', b)
    cv2.waitKey(1)

    # 显示LBP图像
    print('LBP...')
    gray_fg = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    fg_lbp = np.uint8(local_binary_pattern(gray_fg, 8 * 3, 3))
    gray_bg = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
    bg_lbp = np.uint8(local_binary_pattern(gray_bg, 8 * 3, 3))
    cv2.imshow('foreground-lbp', fg_lbp)
    cv2.imshow('background-lbp', bg_lbp)
    cv2.waitKey(1)

    # 准备字典
    print('Connecting to database...')
    db = get_db()
    dictionaries = db.dictionaries
    dictionary = dictionaries.find_one({'library': dict_name})
    if dictionary is None:
        raise UnknownLibraryError(dict_name)

    # 提取特征
    print('Get image feature...')
    f_h, f_s, f_lbp = base_hist(f, b_area)
    b_h, b_s, b_lbp = base_hist(b, f_area)
    sift_hist = sift_count(f, np.array(dictionary['dictionary']))

    data = [f_h, f_s, f_lbp, sift_hist, b_h, b_s, b_lbp]
    for i in range(len(HIST_NAMES)):
        plt.figure(i)
        plt.title(HIST_NAMES[i])
        plt.bar(np.arange(len(data[i])), data[i])

    print('Done!')
    plt.show()
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i, --image', action='store', dest='image', required=True, help='Image path.')
    parser.add_argument('-d, --dict', action='store', dest='dict', required=True, help='Dictionary\'s name.')
    # 读取参数
    params = parser.parse_args()
    print('Start...')
    test(params.image, params.dict)
