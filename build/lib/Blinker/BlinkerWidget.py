# -*- coding: utf-8 -*-

"""
"""

__author__ = 'stao'


class BlinkerButton(object):
    """ """

    def __init__(self, name, func=None):
        self.name = name
        if func:
            self.func = func
        else:
            self.func = None
        self.color = None
        self.text = None

    def attach(self, func):
        self.func = func

    def color(self, color):
        self.color = color

    def text(self, text):
        self.text = text

    def print(self):
        pass
