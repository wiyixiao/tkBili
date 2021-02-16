#!/usr/bin/python3
# -*- coding: utf-8 -*-
import subprocess

from src.custom.WorkTypeEnum import WorkType
from src.utils.File import File
from src.utils.Util import Util
from src.views.BaseFrame import BaseFrame

from PIL import ImageTk, Image
# import pyaudio
import numpy as np
#from moviepy.editor import VideoFileClip
# from ffpyplayer.player import MediaPlayer
# from src.custom.Player import Player

import tkinter as tk
import re
import json
import time
import os
import vlc
import ctypes
# import cv2

## https://www.jianshu.com/p/091282b4353e?utm_campaign=maleskine&utm_content=note&utm_medium=seo_notes&utm_source=recommendation

video_info = 'video:0/0'
audio_info = 'audio:0/0'
video_name = 'merge'

VIDEOWIDTH = 320
VIDEOHEIGHT = 240
buf = None
buf_p = None

class PlayerFrame(BaseFrame):
    def __init__(self, parent, root):
        super(PlayerFrame, self).__init__(parent, root)
        self.video_down_state = False
        self.audio_down_state = False
        self.exit_flag = False
        self.player = None
        # vlc
        # --noaudio
        # --novideo
        # --no3dn
        # "--audio-visual=visual", "--effect-list=spectrum", "--effect-fft-window=flattop"
        # --vout={any,direct3d11,direct3d9,glwin32,gl,directdraw,wingdi,caca,vdummy,vmem,flaschen,yuv,vdummy,none}
        # self.player = Player()
        self._init_ui()
        self._init_vlc()

    def _init_ui(self):
        self.label_video = tk.Label(self, text=video_info)
        self.label_video.pack()
        self.label_video.config(pady=2, padx=2)
        self.label_audio = tk.Label(self, text=audio_info)
        self.label_audio.pack()
        self.label_audio.config(pady=2, padx=2)
        # 视频帧
        global canvas
        # self._canvas = tk.Canvas(self, bg="orange")
        # canvas = self._canvas
        self._canvas = tk.Label(self)
        self._canvas.pack(fill=tk.BOTH)
        canvas = self._canvas

    def _init_vlc(self):
        global buf, buf_p
        self.mp = None
        self.vlcInstance = vlc.Instance()
        self.size = VIDEOWIDTH * VIDEOHEIGHT * 4
        buf = (ctypes.c_ubyte * self.size)()
        buf_p = ctypes.cast(buf, ctypes.c_void_p)

    VideoLockCb = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p))
    @VideoLockCb
    def _lockcb(opaque, planes):
        global buf_p
        # print("lock", file=sys.stderr)
        planes[0] = buf_p

    def init_focus(self, bvid):
        url = f"https://www.bilibili.com/video/{bvid}"
        try:
            self.params['url'] = url
            self.params['element'] = ''
            self.params['call'] = self.get_video_url
            self.params['type'] = WorkType.GET_JSON
            self.web_work(self.params)

        except Exception as e:
            print(e)

    def get_video_url(self, context):
        # print(context)
        self.video_down_state = False
        self.audio_down_state = False
        self.label_video.config(text=video_info)
        self.label_audio.config(text=audio_info)
        self.label_video.pack()
        self.label_audio.pack()
        self._canvas.focus_set()
        self._canvas.pack_forget()
        self.exit_flag = False
        # .*表示任意匹配除换行符（\n、\r）之外的任何单个或多个字符
        # '<script>window.__playinfo__=(.*?)</script>'
        urlPattern = r'\<script\>window\.__playinfo__=(.*?)\</script\>'
        result = re.findall(urlPattern, context, re.S)[0]
        html_data = json.loads(result)
        # print(html_data)
        # Referer:https://www.bilibili.com/
        video_url = html_data['data']['dash']['video'][2]['baseUrl']
        audio_url = html_data['data']['dash']['audio'][2]['baseUrl']
        print(video_url)
        # print(audio_url)

        # 下载视频
        self.params['url'] = video_url
        self.params['element'] = ''
        self.params['call'] = self.video_down_load
        self.params['type'] = WorkType.GET_CONTENT
        self.web_work(self.params)
        # 下载音频
        self.params['url'] = audio_url
        self.params['element'] = ''
        self.params['call'] = self.audio_down_load
        self.params['type'] = WorkType.GET_CONTENT
        self.web_work(self.params)
        # 合成
        self.thread_pool.run(self.video_audio_merge_single, (1,), None)

    def video_down_load(self, video_content):
        try:
            video_size = 0
            mp4_file_size = int(video_content.headers['content-length'])
            if video_content.status_code == 200:
                print('video [文件大小]:%0.2f MB' % (mp4_file_size / 1024 / 1024))
                with open('tmp.mp4', mode='wb') as mp4:
                    for chunk in video_content.iter_content(chunk_size=1024):
                        if chunk:
                            mp4.write(chunk)
                            video_size += len(chunk)  # 已下载的文件大小
                            self.label_video.config(text=f"video: {video_size}/{mp4_file_size}")
                            # print(video_size)

                        if self.exit_flag:
                            break
                print('下载完成')
                self.video_down_state = True
        except Exception as e:
            print('下载失败')

    def audio_down_load(self, audio_content):
        try:
            audio_size = 0
            sound_file_size = int(audio_content.headers['content-length'])
            if audio_content.status_code == 200:
                print('audio [文件大小]:%0.2f MB' % (sound_file_size / 1024 / 1024))
                with open('tmp.mp3', mode='wb') as mp3:
                    for chunk in audio_content.iter_content(chunk_size=1024):
                        if chunk:
                            mp3.write(chunk)
                            audio_size += len(chunk)  # 已下载的文件大小
                            self.label_audio.config(text=f"audio: {audio_size}/{sound_file_size}")
                            if self.exit_flag:
                                break
                print('下载完成')
                self.audio_down_state = True
        except Exception as e:
            print('下载失败')

    def video_audio_merge_single(self, a):
        # 删除上一次合成文件
        File.del_file_subfix("../data/", ['mp4','mp3'])
        # 等待下载完成
        while self.video_down_state == False or self.audio_down_state == False:
            print("下载中...")
            time.sleep(2)
            if self.exit_flag:
                return
        self.label_audio.pack_forget()
        # 合成视频
        print('视频合成开始：', video_name)
        self.label_video.config(text="合成中...")
        time.sleep(1)

        ffm = 'ffmpeg '
        system = Util.get_platform()

        if system == 'Windows':
            # ffm = fr"{self.project_root}\src\3rdParty\ffmpeg_win\bin\ffmpeg.exe "
            ffm = fr"{self.conf.read_val('LIB', 'lib_ffmpeg')} "
        # command = ffm + '-i "{}.mp4" -i "{}.mp3" -vcodec copy -acodec copy "../data/tmp.mp4" -vf scale=320:240 \
        #                 "../data/{}.mp4"'.format(
        #     'tmp', 'tmp', video_name)
        command = ffm + '-i "{}.mp4" -i "{}.mp3" -vcodec copy -acodec copy "../data/{}.mp4"'.format(
            'tmp', 'tmp', video_name)
        # subprocess.Popen(command, shell=True)
        child = subprocess.Popen(command, stderr=subprocess.PIPE, universal_newlines=True, shell=True)

        # child.poll()判断子进程是否结束
        while child.poll() is None:
            line = child.stderr.readline().strip()
            if self.exit_flag == True:
                break
            if line:
                # 在此可以获取到ffmpeg每一次的信息输出
                print(line)

        # ffmpeg进程结束，关闭流
        child.stderr.close()
        print("视频合成结束：", video_name)
        self.label_video.config(text="合成结束")
        time.sleep(1)
        os.remove(f'tmp.mp3')
        os.remove(f'tmp.mp4')

        # 隐藏控件
        self.label_video.pack_forget()
        # 显示视频帧
        self._canvas.pack()
        self._canvas.focus_set()

        if self.exit_flag == False:
            # 开启播放线程
            # self.player.play(f'../data/{video_name}.mp4')
            print('开始播放')

            self.m = self.vlcInstance.media_new(f'../data/{video_name}.mp4')
            self.mp = vlc.libvlc_media_player_new_from_media(self.m)

            vlc.libvlc_video_set_callbacks(self.mp, self._lockcb, None, self._display, None)
            self.mp.video_set_format("BGRA", VIDEOWIDTH, VIDEOHEIGHT, VIDEOWIDTH * 4)

            while True:
                if self.exit_flag:
                    self.mp.stop()
                    break
                self.mp.play()
                time.sleep(1)

            print('退出播放线程')

    def close_network(self):

        self.exit_flag = True

        # self.player.close_player()
        self._canvas.pack_forget()

    def is_play(self):
        return self.exit_flag

    def get_canvas(self):
        return

    @vlc.CallbackDecorators.VideoDisplayCb
    def _display(opaque, picture):
        global buf
        img = Image.frombuffer("RGBA", (VIDEOWIDTH, VIDEOHEIGHT), buf, "raw", "BGRA", 0, 1)
        imgtk = ImageTk.PhotoImage(image=img)
        canvas.config(image=imgtk)
        canvas.imgtk = imgtk
        canvas.update()



