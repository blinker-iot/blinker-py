# -*- coding: utf-8 -*-

"""
mqtt数据处理
"""

__author__ = 'stao'

from blinker import Device


def data_read_func():
    print(device.data_reader.get())


device = Device("authKey", protocol="mqtts", ready_func=data_read_func)

if __name__ == '__main__':
    device.run()
