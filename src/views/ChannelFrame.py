#!/usr/bin/python3
# -*- coding: utf-8 -*-
from src.custom.WorkTypeEnum import WorkType
from src.views.BaseFrame import BaseFrame

import tkinter as tk

import json
import math

from src.views.PagesEnum import Pages

SMALL_FONT = ("Verdana", 10)

# 请求接口地址
x_base_api = 'https://api.bilibili.com/x/web-interface/newlist?'


class ChannelFrame(BaseFrame):
    def __init__(self, parent, root):
        super(ChannelFrame, self).__init__(parent, root)
        self.listbox = None
        self.root = root
        self.page_count = 0
        self.pn = 1  # 默认请求页
        self.ps = 20  # 单页条目数
        self.rid = '-1'  # 二级分区编号
        self.content_list = []  # 存储视频列表数据
        self._init_ui()

    def _init_ui(self):
        self.sb = tk.Scrollbar(self)
        self.sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox = tk.Listbox(self, yscrollcommand=self.sb.set)
        self.listbox.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH, padx=5)
        self.sb.config(command=self.listbox.yview)

        self.page_label = tk.Label(self, text='', font=SMALL_FONT)
        self.page_label.pack()

        # 绑定事件
        self.listbox.bind("<KeyPress-u>", self.page_prev)
        self.listbox.bind("<KeyPress-i>", self.page_next)
        self.listbox.bind("<KeyPress-j>", self.open_player)

    def init_focus(self, url, rid):
        if self.listbox is not None:
            self.listbox.focus_set()
            self.listbox.delete(0, tk.END)
            self.listbox.select_set(0)
            self.content_list.clear()

            rid = rid.strip()

            if rid == '-1':
                self.listbox.insert(tk.END, 'no data')
                return
            else:
                self.listbox.insert(tk.END, 'waiting ...')
                self.rid = rid

            # 拼接请求地址
            request_url = x_base_api + ("rid=%s&pn=%d&ps=%d" % (self.rid, self.pn, self.ps))
            print(request_url)

            # 获取json数据
            self.params['url'] = request_url
            self.params['element'] = ''
            self.params['call'] = self.channel_list_count
            self.params['type'] = WorkType.GET_JSON
            self.web_work(self.params)



    def channel_list_count(self, rjson):
        # json数据解析
        try:
            # 获取分页数量
            page = json.loads(rjson)['data']['page']
            self.calc_page_count(page)
            # 获取单页数据
            data = json.loads(rjson)['data']['archives']
            self.channel_list_parser(data)
        except Exception as e:
            print(e)

    def calc_page_count(self, page_info):
        count = page_info['count']
        self.page_count = math.ceil(count / self.ps)
        print(self.page_count)
        print(page_info['num'])

        # 设置页数标签
        self.page_label.config(text=("共 %s 页/ %s 个 -- 当前 %d 页" % (self.page_count, count, self.pn)))

    def channel_list_parser(self, page_data):
        try:
            self.content_list.clear()
            self.listbox.delete(0, tk.END)

            for j in range(len(page_data)):
                content = {}
                # 此处只获取标题以及视频时长
                content['title'] = page_data[j]['title']
                content['duration'] = page_data[j]['duration']
                content['bvid'] = page_data[j]['bvid']
                self.listbox.insert(tk.END, ("%s -- %s" % (content['duration'], content['title'])))
                # 添加到列表
                self.content_list.append(content)

        except Exception as e:
            print(e)

    # 上一页
    def page_prev(self, event):
        self.pn -= 1
        self.pn = max(1, self.pn)
        self.init_focus('', self.rid)

    # 下一页
    def page_next(self, event):
        self.pn += 1
        self.pn = min(self.pn, self.page_count)
        self.init_focus('', self.rid)

    def open_player(self, event):
        try:
            count = len(self.content_list)
            if count <= 0:
                print("list is null")
                return
            index = self.listbox.curselection()[0]
            self.root.show_frame(Pages.PLAYER, None, None, self.content_list[index]['bvid'])
        except Exception as e:
            print(e)
