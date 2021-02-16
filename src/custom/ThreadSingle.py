#!/usr/bin/python3
# -*- coding: utf-8 -*-

from threading import Thread


class tkThread(Thread):
    def __init__(self, target=None,
                 args=(), kwargs=None):
        super().__init__()
        if kwargs is None:
            kwargs = {}
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.target(*self.args, **self.kwargs)
