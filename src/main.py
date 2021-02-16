#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys

from src.utils.Util import Util

sys.path.append("..")

from src.custom.IniWr import IniWr
from src.views.FrameManager import FrameManager

# 全局变量
import src.vars.GlobalManager as gm

# 配置文件路径
CONFIG_PATH = '../docs/conf.ini'

# 初始化全局变量
gm._init()
gm.set_value('conf', IniWr(CONFIG_PATH))

# 读取配置文件
conf = gm.get_value('conf')

vlc_path = conf.read_val('LIB', 'lib_vlc')
print(vlc_path)
if Util.get_platform() == 'Windows':
    os.environ['PYTHON_VLC_MODULE_PATH'] = vlc_path

# 初始化界面
app = FrameManager(conf, False)


def run():
    app.mainloop()
