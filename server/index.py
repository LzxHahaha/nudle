from flask import Flask
from flask import jsonify
import cv2

from core.sift import sift, __core

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
