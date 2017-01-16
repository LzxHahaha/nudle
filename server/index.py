import json

import cv2
from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy
from PIL import Image
from skimage import io

from core.search import search

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/search/upload', methods=['POST'])
def upload_search():
    library = request.args.get('library', 'voc2006')
    image_file = request.files.get('image', None)
    image = numpy.asarray(Image.open(image_file.stream))
    result, save = search(image, library)
    if save:
        pass
    return jsonify({'result': result})


@app.route('/api/search/url', methods=['POST'])
def url_search():
    params = json.loads(request.data)
    library = 'voc2006'
    url = params['url']
    image = io.imread(url)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    result, save = search(image, library)
    if save:
        pass
    return jsonify({'result': result})


if __name__ == '__main__':
    app.run()
