#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
import time


from src.views.BaseFrame import BaseFrame

from src.custom.WorkTypeEnum import WorkType
from src.views.PagesEnum import Pages

LARGE_FONT = ("Verdana", 12)

# 主站目录
url = 'https://www.bilibili.com/'
# 二级分区编号
rid_list = [
    '24','25','47','210','86','27',
    '33','32','51','152','-1','-1',
    '28','31','30','194','59','193','29','130','-1','-1',
    '153','168','169','195','170','-1','-1',
    '20','198','199','200','154','156',
    '17','171','172','65','173','121','136','19','-1',
    '201','124','207','208','209','122',
    '95','189','190','191',
    '138','21','75','161','162','163','176','174',
    '22','26','126','216','127',
    '157','158','164','159','192',
    '203','204','205','206',
    '71','137',
    '182','183','85','184',
    '-1','-1','-1'
]


class HomeFrame(BaseFrame):
    def __init__(self, parent, root):
        super(HomeFrame, self).__init__(parent, root)
        self.root = root
        self.channel_links = []
        self._init_ui()

    def _init_ui(self):
        self.sb = tk.Scrollbar(self)
        self.sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox = tk.Listbox(self, yscrollcommand=self.sb.set)
        self.listbox.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH, padx=5)
        self.sb.config(command=self.listbox.yview)

        # 绑定分页切换事件
        self.listbox.bind("<KeyPress-j>", self.open_channel)

    def init_focus(self):
        if self.listbox is not None:
            self.listbox.focus_set()
            self.listbox.delete(0, tk.END)
            self.listbox.insert(tk.END, 'waiting ...')
            self.listbox.select_set(0)

            # 获取链接列表
            self.params['url'] = url
            self.params['element'] = 'div.sub-container .sub-item a'
            self.params['call'] = self.channel_list_set
            self.params['type'] = WorkType.GET_ELEMENT
            self.web_work(self.params)

    # 更新列表
    def channel_list_set(self, reslist):
        # 清空
        self.listbox.delete(0, tk.END)
        self.channel_links.clear()
        # 序号
        index = 0
        # 添加到列表
        for a in reslist:
            self.channel_links.append(list(a.absolute_links)[0])
            self.listbox.insert(tk.END, ("%s -- %s" % (a.text, rid_list[index])))
            index+=1

        self.listbox.select_set(0)

    def open_channel(self, event):
        select_index = self.listbox.curselection()[0] # 单选
        # 跳转页面至当前分类视频列表页
        self.root.show_frame(Pages.CHANNEL, self.channel_links[select_index], rid_list[select_index])





