# coding=utf-8
import base64

import cv2
from flask import Flask, request
from flask import render_template
from flask_cors import CORS
import time
import re
import urllib.request
import numpy as np

from core.SaliencyaBoF import SaliencyBoF
from utils import mongo
from utils.helper import convert_from, error_handler, to_jpg, convert_to
from utils.json import success, failed
import config
from utils.mongo import get_db
from exceptions import *

app = Flask(__name__)

if config.DEV:
    print('==========================\n*  Development mode: ON  *\n==========================')
    # 仅DEV下允许API跨域
    CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/api/libraries', methods=['GET'])
@error_handler
def get_all_libraries():
    db = get_db()
    names = db.collection_names()
    res = []
    # 找出所有图片库名并返回
    for name in names:
        lib_name = re.findall(r"images_(.+)", name)
        if len(lib_name) == 1:
            res.append(lib_name[0])
    return success({'libraries': res})


@app.route('/api/search/upload', methods=['POST'])
@error_handler
def upload_search():
    library = request.form.get('library', 'voc2006')
    image_b64 = request.form.get('image', None)
    size = int(request.form.get('size', 20))

    # base64 转码
    image, image_type = convert_from(image_b64)

    # 查找
    start_time = time.time()
    result, histograms, mask = SaliencyBoF.search(image, library, size)
    search_time = time.time() - start_time

    return success({
        'list': result,
        'histograms': histograms,
        'search_time': search_time,
        'rc_mask': convert_to(mask),
        'height': image.shape[0],
        'width': image.shape[1],
        'type': image_type
    })


@app.route('/api/search/url', methods=['POST'])
@error_handler
def url_search():
    library = request.form.get('library', 'voc2006')
    url = request.form.get('url', None)
    size = int(request.form.get('size', 20))

    # 获取网络图片
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    # 判断类型是否为图片
    content_type = response.getheader('Content-Type')
    image_type = re.match(r"^image/(\w+)$", content_type)
    if image_type is None:
        raise UnknownImageError(content_type)
    # 判断是否需要转换为JPG
    image_type = image_type.group(1).lower()
    image_bytes = response.read()
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), 1)
    if image_type not in ['jpg', 'jpeg']:
        image = to_jpg(image)

    start_time = time.time()
    result, histograms, mask = SaliencyBoF.search(image, library, size)
    search_time = time.time() - start_time

    return success({
        'list': result,
        'histograms': histograms,
        'search_time': search_time,
        'rc_mask': convert_to(mask),
        'height': image.shape[0],
        'width': image.shape[1],
        'type': image_type
    })


@app.route('/api/image/<lib>/<name>', methods=['GET'])
@error_handler
def image_detail(lib, name):
    if name is None or lib is None:
        return failed(400, 'Wrong parameter.')
    doc = mongo.get_db()['images_' + lib]
    if doc is None:
        return failed(404, 'Unknown library.')
    data = doc.find({'name': name}, {'_id': 0})
    if data.count() < 1:
        return failed(404, 'Unknown image.')
    result = data[0]

    return success(result)


if __name__ == '__main__':
    if not config.DEV:
        print('WARNING: Now is dev mode, do NOT use it in the production environment.')
    app.run(port=5001)
