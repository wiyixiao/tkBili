#!/usr/bin/python3
# -*- coding: utf-8 -*-

class GlobalVar:
    _global_dict = None

def _init():  # 初始化
    GlobalVar._global_dict = {}


def set_value(key, value):
    """ 定义一个全局变量 """
    GlobalVar._global_dict[key] = value


def get_value(key, defValue=None):
    """ 获得一个全局变量,不存在则返回默认值 """
    try:
        return GlobalVar._global_dict[key]
    except KeyError:
        return defValue