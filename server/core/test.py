# coding=utf-8
import cv2

from core.saliency_cut import cut


image = cv2.imread('D:\\Works\\Code\\image-retrieval\\server\\static\\voc2006\\000003.png')
f, b = cut(image)
cv2.imshow('f', f)
cv2.imshow('b', b)
cv2.waitKey(0)
cv2.destroyAllWindows()
