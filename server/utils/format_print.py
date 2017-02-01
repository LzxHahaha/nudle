# coding=utf-8
import datetime


def datetime_print(s):
    now = datetime.datetime.now()
    print '[%s]\t%s' % (now.strftime('%Y-%m-%d %H:%M:%S'), s)
