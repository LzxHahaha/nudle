# coding=utf-8

import cv2
import saliency_rc_cut


def cut(image):
    mask = saliency_rc_cut.cut(image)
    mask = cv2.threshold(mask, 1, 1, cv2.THRESH_BINARY)[1]
    foreground = cv2.bitwise_and(image, image, mask=mask)
    mask = (mask - 1)
    background = cv2.bitwise_and(image, image, mask=mask)
    return foreground, background
