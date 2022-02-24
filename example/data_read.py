# -*- coding: utf-8 -*-

"""
mqtt其它数据处理
"""

__author__ = 'stao'

from blinker import Device


def data_read_func():
    print(device.data_reader.get())


device = Device("authKey", protocol="mqtts", init_ready_func=data_read_func)

if __name__ == '__main__':
    device.run()
