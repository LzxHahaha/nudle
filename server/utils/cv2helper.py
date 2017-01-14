# coding=utf-8
import cv2


def try_load(img):
    if isinstance(img, basestring):
        image = cv2.imread(img)
        if image is None:
            raise Exception('Unknown image')
        return image
    return img
