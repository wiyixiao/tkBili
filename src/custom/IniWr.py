#!/usr/bin/python3
# -*- coding: utf-8 -*-
import configparser


class IniWr(object):
    def __init__(self, path):
        super(IniWr, self).__init__()
        self.path = path
        self.conf = configparser.ConfigParser()
        print(path)

        # 读取文件
        if len(self.path) > 0:
            self.conf.read(self.path, encoding="utf-8")  # python3
            # self.conf.read(self.path)  # python2
        else:
            print('配置文件路径错误')

    def read_val(self, section, key=None):
        try:
            if key is None:
                return self.conf[section]
            return self.conf[section][key]
        except Exception as e:
            return None

    def write_val(self, section, option, val):
        secs = self.read_val(section)
        if secs is None:
            print('没有找到 %s' % section)
            self.conf.add_section(section)
            print('添加成功 %s' % section)

        self.conf.set(section, option, val)
        self.conf.write(open(self.path, "w"))

    def del_option(self, section, option):
        secs = self.read_val(section)

        if secs is None:
            print('没有找到，删除失败')
        else:
            self.conf.remove_option(section, option)
            print('删除成功')

        self.conf.write(open(self.path, "w"))

    def get_sections(self):
        return self.conf.sections()
