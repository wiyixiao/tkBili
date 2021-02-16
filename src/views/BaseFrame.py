#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import tkinter as tk
import src.vars.GlobalManager as gm

from requests_html import HTMLSession

from src.custom.ThreadPool import tkThreadPool
from src.custom.WorkTypeEnum import WorkType

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'https://www.bilibili.com/',
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection': 'keep-alive',
    # 'Cookie':cookie
}


class BaseFrame(tk.Frame):
    def __init__(self, parent, root):
        super(BaseFrame, self).__init__(parent)
        self.headers = headers
        self.params = {
            'url':None,
            'element':None,
            'call':None,
            'type':None
        }
        self.conf = gm.get_value('conf')  # 配置文件
        self.session = HTMLSession()
        self.project_root = os.path.abspath(os.path.join(os.getcwd(), ".."))
        self.thread_pool = tkThreadPool(5)

    def web_work(self, args):
        vars = (args['url'], args['element'], args['call'], args['type'])
        self.thread_pool.run(self.action, vars, self.callback)

    def action(self, url, ele, call, type):
        res = self.session.get(url, headers=self.headers)

        if res.status_code != 200:
            print('load url failed')
            return

        if type == WorkType.GET_ELEMENT:
            call(res.html.find(ele))
        elif type == WorkType.GET_JSON:
            call(res.content.decode('utf8'))
        elif type == WorkType.GET_CONTENT:
            call(res)
        elif type == WorkType.GET_NONE:
            call(True)

    def callback(self, status, result):
        # status, execute action status
        # result, execute action return value
        pass

    def close(self):
        self.thread_pool.close()

