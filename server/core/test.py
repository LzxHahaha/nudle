# coding=utf-8
import cv2

from core.saliency import cut

image = cut('D:\\Works\\Code\\image-retrieval\\server\\static\\voc2006\\000003.png')
# print 'res:%d' % image
cv2.imshow('image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
