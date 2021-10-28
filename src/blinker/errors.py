# -*- coding: utf-8 -*-

"""
"""

__author__ = 'stao'


class BlinkerException(Exception):
    def __init__(self, message: int, detail: str = ""):
        self.errCode = message
        self.detail = detail


class BlinkerHttpException(BlinkerException):
    pass


class BlinkerBrokerException(BlinkerException):
    pass
