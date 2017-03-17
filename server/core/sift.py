# coding=utf-8
import cv2

from utils.helper import try_load


cv2sift = cv2.xfeatures2d.SIFT_create()


def sift(img):
    image = try_load(img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2sift.detectAndCompute(gray, None)
