# coding=utf-8
import cv2
import re
import base64
import numpy as np
from functools import wraps
import pymongo.errors

from exceptions import *
from .json import failed, error


def try_load(img):
    if isinstance(img, str):
        image = cv2.imread(img)
        if image is None:
            raise UnknownImageError('None')
        return image
    return img


def to_jpg(image):
    ret, buf = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 100])
    return cv2.imdecode(buf, 1)

ACCEPT_TYPES = ['png', 'jpeg']


def convert_from(base64_str):
    try:
        match_result = re.match(r"^data:image/(\w{,4});base64,(.+)$", base64_str)
        if match_result is not None:
            file_type = match_result.group(1)
            content = match_result.group(2)
            if file_type not in ACCEPT_TYPES:
                raise UnknownImageError(file_type)
            image_data = base64.b64decode(content)
            image_data = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(image_data, 1)
            if file_type == 'png':
                image = to_jpg(image)
            return image
        raise UnknownImageError()
    except Exception:
        raise


def error_handler(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except pymongo.errors.ServerSelectionTimeoutError:
            return failed(504, 'Database Connect time out.')
        except Exception as e:
            if hasattr(e, 'code') and hasattr(e, 'message'):
                return failed(e.code, e.message)
            else:
                return error(500)
    return decorated_function
