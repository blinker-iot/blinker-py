# -*- coding: utf-8 -*-

"""
日志存储示例
"""

__author__ = 'stao'

from blinker import Device


async def ready_func():
    while True:
        log = "This is log test"
        await device.saveLogData(log)


device = Device("authKey", protocol="mqtts", ready_func=ready_func)

if __name__ == '__main__':
    device.run()
