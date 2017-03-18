# coding=utf-8

import cv2
import numpy as np
import saliency_cut


def cut(image, custom_mask=None):
    # 可选传入一个mask
    if custom_mask is None:
        mask = saliency_cut.rc_mask(image)
    else:
        mask = custom_mask.copy()

    # 无法裁剪的情况，都当作前景处理
    if mask is None:
        foreground = image
        background = None
        fg_area = image.size
        bg_area = 0
    # 裁剪图像，计算前景与背景的面积
    else:
        mask = cv2.threshold(mask, 1, 1, cv2.THRESH_BINARY)[1]
        fg_area = np.sum(mask)
        bg_area = mask.size - fg_area
        foreground = cv2.bitwise_and(image, image, mask=mask)
        mask = (mask - 1)
        mask = cv2.threshold(mask, 1, 1, cv2.THRESH_BINARY)[1]
        background = cv2.bitwise_and(image, image, mask=mask)
    return foreground, background, fg_area, bg_area
