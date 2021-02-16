#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os,sys,platform


class File(object):
    def __init__(self):
        super(File, self).__init__()

    @staticmethod
    def removeFile(path, remove_list, retain_list):  # path后面要跟/
        path = path
        system_test = platform.system()
        if system_test == 'Windows':
            path_last = path[-1]
            if path_last != '\\':
                path = path + '\\'
        elif system_test == 'Linux':
            path_last = path[-1]
            if path_last != '/':
                path = path + '/'
        if len(remove_list) == 0 and len(retain_list) == 0:  # 如果remove_list,retain_list都是空则删除path目录下所有文件及文件夹
            File.remove_file(File.eachFile(path))
        elif len(remove_list) > 0 and len(retain_list) == 0:
            File.remove_file(remove_list)
        elif len(remove_list) == 0 and len(retain_list) > 0:
            list = File.eachFile(path)
            for f in retain_list:
                if (f in list):
                    list.remove(f)
                else:
                    print('There is no file in the directory!')
            File.remove_file(list)
        elif (len(remove_list) > 0 and len(retain_list) > 0):
            for f in retain_list:
                if (f in remove_list):
                    remove_list.remove(f)
            File.remove_file(remove_list)

    @staticmethod
    def remove_file(file_list, path = None):
        for filename in file_list:
            if (os.path.exists(path + filename)):  # 判断文件是否存在
                if (os.path.isdir(path + filename)):
                    File.del_file(path + filename)
                else:
                    if (os.path.exists(path + filename)):
                        os.remove(path + filename)
            else:
                print(path + filename + ' is not exist!')
        for filename in file_list:
            if (os.path.exists(path + filename)):
                File.del_dir(path + filename)

    @staticmethod
    def del_file(path):  # 递归删除目录及其子目录下的文件
        for i in os.listdir(path):
            path_file = os.path.join(path, i)  # 取文件绝对路径
            if os.path.isfile(path_file):  # 判断是否是文件
                os.remove(path_file)
            else:
                File.del_file(path_file)


    @staticmethod
    def del_dir(path):  # 删除文件夹
        for j in os.listdir(path):
            path_file = os.path.join(path, j)  # 取文件绝对路径
            if not os.listdir(path_file):  # 判断文件如果为空
                os.removedirs(path_file)  # 则删除该空文件夹，如果不为空删除会报异常
            else:
                File.del_dir(path_file)

    @staticmethod
    def eachFile(filepath):  # 获取目录下所有文件的名称
        pathDir = os.listdir(filepath)
        list = []
        for allDir in pathDir:
            child = os.path.join('%s%s' % (filepath, allDir))
            fileName = child.replace(filepath, '')
            list.append(fileName)
        return list

    @staticmethod
    def del_file_subfix(path, subfix):
        print(subfix)
        list = File.eachFile(path)

        if list is not None:
            for fname in list:
                if os.path.splitext(fname)[1][1:] in subfix:
                    print(f'{path}{fname}')
                    os.remove(f'{path}{fname}')
                else:
                    print('no file')

        print('del file success')
