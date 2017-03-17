# coding=utf-8
import cv2
from flask import Flask, request
from flask import render_template
from flask_cors import CORS
from skimage import io
import time
import re

from core.search import search
from utils.helper import convert_from, error_handler
from utils.json import success
import config
from utils.mongo import get_db

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
    size = request.form.get('size', 20)

    # base64 转码
    image = convert_from(image_b64)

    # 查找
    start_time = time.time()
    result, histograms = search(image, library, size)
    search_time = time.time() - start_time

    return success({
        'list': result,
        'histograms': histograms,
        'search_time': search_time
    })


@app.route('/api/search/url', methods=['POST'])
@error_handler
def url_search():
    library = request.form.get('library', 'voc2006')
    url = request.form.get('url', None)
    size = request.form.get('size', 20)

    # 下载图片
    image = io.imread(url)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    start_time = time.time()
    result, histograms = search(image, library, size)
    search_time = time.time() - start_time

    return success({
        'list': result,
        'histograms': histograms,
        'search_time': search_time
    })


if __name__ == '__main__':
    if not config.DEV:
        print('WARNING: Now is dev mode, do NOT use it in the production environment.')
    app.run()
