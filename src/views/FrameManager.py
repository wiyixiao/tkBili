#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import tkinter as tk

from src.utils.Util import Util
from src.views.HelpFrame import HelpFrame
from src.views.HomeFrame import HomeFrame
from src.views.ChannelFrame import ChannelFrame
from src.views.SettingFrame import SettingFrame
from src.views.PlayerFrame import PlayerFrame

from src.views.PagesEnum import Pages

frames = []
frame_id = Pages.HOME
frame_last_id = Pages.HOME
frame_url = ''
frame_rid = ''


class FrameManager(tk.Tk):
    def __init__(self, cfg, border):
        super().__init__()
        self.cfg = cfg
        w = self.cfg.read_val('GUI', 'win_width')
        h = self.cfg.read_val('GUI', 'win_height')
        self.geometry('%sx%s' % (w, h))  # 设置窗口大小
        self.overrideredirect(border)  # 无边框
        self.maxsize(w, h)  # 窗口限制
        self.minsize(w, h)
        self.top_frame = None
        self.update()
        self._init_frames()
        self._init_menu()

    def _init_frames(self):
        self.container = tk.Frame(self)
        self.container.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # 初始化窗口
        for F in (HomeFrame, ChannelFrame, PlayerFrame, SettingFrame, HelpFrame):
            frame = F(self.container, self)
            frames.append(frame)
            frame.grid(row=0, column=0, sticky=tk.NSEW)

        # 初始显示主页面
        self.show_frame(Pages.HOME)

    def _init_menu(self):
        self.menubar = tk.Menu(self, tearoff=False, postcommand=self.menu_open_callback)

        self.menubar.add_command(label='Home', command=self.home_menu_click)
        self.menubar.add_command(label='Refresh', command=self.refresh_click)
        # self.menubar.add_command(label='Setting', command=self.setting_menu_click)
        self.menubar.add_command(label='Help', command=self.help_menu_onclick)
        self.menubar.add_command(label='Exit', command=self.exit_onclick)

        self.bind("<Return>", self.menu_open)
        self.menubar.bind("<Escape>", self.exit_onclick)
        self.bind("<Escape>", self.exit_onclick)
        self.bind("<KeyPress>", self.keypress_onclick)  # 绑定按键监听

    def menu_open(self, event):
        # x: event.x_root
        # y: event.y_root
        pos = Util.get_screen_pos(self)

        # 部分页面禁用刷新按钮
        if frame_id == Pages.SETTING or frame_id == Pages.HELP or frame_id == Pages.PLAYER:
            self.menubar.entryconfig("Refresh", state=tk.DISABLED)
        else:
            self.menubar.entryconfig("Refresh", state=tk.NORMAL)
        # 指定位置弹出菜单
        self.menubar.post(pos[0] + 100, pos[1] + 100)

    def menu_open_callback(self):
        self.menubar.focus_set()  # 按钮菜单获取焦点
        self.menubar.activate(0)

    def setting_menu_click(self):
        self.focus_set()
        self.show_frame(Pages.SETTING)

    def home_menu_click(self):
        self.focus_set()
        frames[Pages.PLAYER].close_network()
        self.show_frame(Pages.HOME)

    def help_menu_onclick(self):
        self.focus_set()
        self.show_frame(Pages.HELP)

    def refresh_click(self):
        self.focus_set()
        self.show_frame(frame_id)

    def exit_onclick(self, event=None):
        for f in frames:
            f.close()
        self.quit()

    # key listener
    def keypress_onclick(self, event):
        key = event.keysym

        '''
        print(frame_id)
        print(frame_last_id)
        '''

        if key == 'k':
            if frame_id == Pages.SETTING or frame_id == Pages.HELP or frame_id == Pages.PLAYER:
                if frame_id == Pages.PLAYER:
                    frames[frame_id].close_network()
                self.show_frame(frame_last_id, frame_url)
            elif frame_id == Pages.CHANNEL:
                self.show_frame(Pages.HOME)
        elif key == 'j':
            if frame_id == Pages.PLAYER:
                pass

    @staticmethod
    def show_frame(id, url=None, rid=None, bvid=None):
        global frame_id, frame_url, frame_last_id, frame_rid
        frame = frames[id]
        frame_last_id = frame_id  # 记录上次的页面ID
        if id == Pages.HOME:
            HomeFrame.init_focus(frame)
        elif id == Pages.CHANNEL:
            frame_url = url
            if rid is not None:
                frame_rid = rid
            ChannelFrame.init_focus(frame, url, frame_rid)
        elif id == Pages.PLAYER:
            PlayerFrame.init_focus(frame, bvid)

        frame.tkraise()  # 切换，提升当前 tk.Frame z轴顺序
        frame_id = id  # 记录当前frame序号
