# coding=utf-8

import cv2
import numpy as np
from saliency_cut import rc_cut


def cut(image):
    mask = rc_cut(image)
    if mask is None:
        foreground = image
        background = None
        fg_area = image.size
        bg_area = 0
    else:
        mask = cv2.threshold(mask, 1, 1, cv2.THRESH_BINARY)[1]
        fg_area = np.sum(mask)
        bg_area = mask.size - fg_area
        foreground = cv2.bitwise_and(image, image, mask=mask)
        mask = (mask - 1)
        mask = cv2.threshold(mask, 1, 1, cv2.THRESH_BINARY)[1]
        background = cv2.bitwise_and(image, image, mask=mask)
    return foreground, background, fg_area, bg_area
