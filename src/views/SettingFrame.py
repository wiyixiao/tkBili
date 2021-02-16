#!/usr/bin/python3
# -*- coding: utf-8 -*-
from src.views.BaseFrame import BaseFrame

import tkinter as tk


class SettingFrame(BaseFrame):
    def __init__(self, parent, root):
        super(SettingFrame, self).__init__(parent, root)
        self._init_ui()

    def _init_ui(self):
        label = tk.Label(self, text="Setting")
        label.pack(pady=10, padx=10)