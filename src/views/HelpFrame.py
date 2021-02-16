#!/usr/bin/python3
# -*- coding: utf-8 -*-
from src.views.BaseFrame import BaseFrame

import tkinter as tk


class HelpFrame(BaseFrame):
    def __init__(self, parent, root):
        super(HelpFrame, self).__init__(parent, root)
        self._init_ui()

    def _init_ui(self):
        label = tk.Label(self, text="V1.0.0\r\nAries.hu\nhttps://www.wiyixiao4.com")
        label.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)






