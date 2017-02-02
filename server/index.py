# coding=utf-8
import cv2
from flask import Flask, request
from flask_cors import CORS
import numpy
from PIL import Image
from skimage import io
import base64
from StringIO import StringIO

from core.search import search
from utils.json import success, failed

app = Flask(__name__)
# 允许API跨域
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/')
def hello_world():
    return 'Hello World!'


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
        result, feature = search(image, library)

        return success({
            'list': result[:size],
            'feature': feature
        })
    except Exception, e:
        return failed(500, e.message)


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

        result, feature = search(image, library)

        return success({
            'list': result[:size],
            'feature': feature
        })
    except Exception, e:
        return failed(500, e.message)


if __name__ == '__main__':
    app.run()
