# -*- coding: utf-8 -*-

"""
mqtt其它数据处理
"""

__author__ = 'stao'

from blinker import Device


async def ready_func():
    print(device.data_reader.get())


device = Device("authKey", ready_func=ready_func)

if __name__ == '__main__':
    device.run()
