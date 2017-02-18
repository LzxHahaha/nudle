# coding=utf-8
from flask import jsonify
import traceback

from config import DEV


def success(value):
    data = {
        'code': 200,
        'data': value
    }
    return jsonify(data)


def failed(code, message='error'):
    data = {
        'code': code,
        'message': message
    }
    return jsonify(data)


def error(code):
    if DEV:
        data = {
            'code': code,
            'message': traceback.format_exc()
        }
    else:
        data = {
            'code': code,
            'message': 'Server error.'
        }
    return jsonify(data)
