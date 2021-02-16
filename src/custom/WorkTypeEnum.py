#!/usr/bin/python3
# -*- coding: utf-8 -*-

from enum import IntEnum


class WorkType(IntEnum):
    GET_ELEMENT = 0             # 获取网页结构
    GET_JSON = 1                # 获取json数据
    GET_CONTENT = 2             # 获取内容
    GET_NONE    = 3             # 非网页操作