# coding=utf-8
import cv2


def try_load(img):
    if isinstance(img, str):
        image = cv2.imread(img)
        if image is None:
            raise Exception('Unknown image')
        return image
    return img


def to_jpg(image):
    ret, buf = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 100])
    return cv2.imdecode(buf, 1)


def convert_from(b64):
    # TODO: parse the string, return image and type (png etc.)
    pass
