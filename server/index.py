import numpy
from PIL import Image
from flask import Flask, jsonify, request
from skimage import io
import base64

from core.search import search

app = Flask(__name__)


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
    library = request.args.get('library', 'voc2006')
    url = request.form.get('url', None)
    image = io.imread(url)
    result, save = search(image, library)
    if save:
        pass
    return jsonify({'result': result})


if __name__ == '__main__':
    app.run()
