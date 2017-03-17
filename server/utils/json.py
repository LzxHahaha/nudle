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


# 已知错误，直接返回自定的错误信息
def failed(code, message='error'):
    data = {
        'code': code,
        'message': message
    }
    return jsonify(data)


# 未知错误，在DEV模式下显示traceback
def error(code=500):
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
