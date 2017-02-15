# coding=utf-8
from ctypes import *


def cut(path):
    dll = cdll.LoadLibrary('./saliency/Saliency.dll')
    return dll.RC_cut_from(path)
