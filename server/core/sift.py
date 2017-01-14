# coding=utf-8
import cv2

from utils.cv2helper import try_load


cv2sift = cv2.SIFT()


# 对SIFT的基本封装，之后如果有特殊需要再考虑修改
def sift(img):
    image = try_load(img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2sift.detectAndCompute(gray, None)
