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
        stack_info = traceback.format_exc()
        print(stack_info)
        data = {
            'code': code,
            'message': stack_info
        }
    else:
        data = {
            'code': code,
            'message': 'Server error.'
        }
    return jsonify(data)
