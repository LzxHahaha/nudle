# coding=utf-8
import cv2
from flask import Flask, request
from flask import render_template
from flask_cors import CORS
import numpy
from PIL import Image
from skimage import io
import base64
from StringIO import StringIO
import time
import pymongo.errors

from core.search import search
from utils.json import success, failed, error
import config


if config.DEV:
    print '==========================\n*  Development mode: ON  *\n=========================='

app = Flask(__name__)
# 允许API跨域
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/test')
def test_page():
    return 'Hello world!'


@app.route('/api/search/upload', methods=['POST'])
def upload_search():
    try:
        library = request.form.get('library', 'voc2006')
        image_file = request.form.get('image', None)
        size = request.form.get('size', 20)

        # base64 转码
        comma_index = image_file.find(',')
        image_file = image_file[comma_index + 1:]
        if image_file is None:
            return failed(404, 'Unknown Image')
        sbuf = StringIO()
        sbuf.write(base64.b64decode(image_file))
        image = Image.open(sbuf)
        image = numpy.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # 查找
        start_time = time.time()
        result, feature = search(image, library)
        search_time = time.time() - start_time

        return success({
            'list': result[:size],
            'feature': feature,
            'search_time': search_time
        })
    except pymongo.errors.ServerSelectionTimeoutError:
        return failed(504, 'Database Connect time out.')
    except Exception:
        return error(500)


@app.route('/api/search/url', methods=['POST'])
def url_search():
    try:
        library = request.form.get('library', 'voc2006')
        url = request.form.get('url', None)
        size = request.form.get('size', 20)
        if url is None:
            return failed(404, 'Unknown Image')

        # 下载图片
        image = io.imread(url)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        start_time = time.time()
        result, feature = search(image, library)
        search_time = time.time() - start_time

        return success({
            'list': result[:size],
            'feature': feature,
            'search_time': search_time
        })
    except pymongo.errors.ServerSelectionTimeoutError:
        return failed(504, 'Database Connect time out.')
    except Exception:
        return error(500)


if __name__ == '__main__':
    if not config.DEV:
        print 'WARNING: Now is dev mode, do NOT use it in the production environment.'
    app.run()
