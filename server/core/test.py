# coding=utf-8
import cv2
import time

from core.search import search

path = 'D:/Works/Code/image-retrieval/server/prepare/voc2006/000013.png'
image = cv2.imread(path)
window_name = 'origin'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, 300, 300)
cv2.imshow(window_name, image)
sort, images = search(image, 'voc2006')
for i in range(16):
    path = 'D:/Works/Code/image-retrieval/server/prepare/voc2006/' + images[sort[i]]
    img = cv2.imread(path)
    window_name = '%d' % i
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 200, 200)
    cv2.imshow(window_name, img)

cv2.waitKey(0)
cv2.destroyAllWindows()
