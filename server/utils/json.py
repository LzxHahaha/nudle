# coding=utf-8
from flask import jsonify


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
