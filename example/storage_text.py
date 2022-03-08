# -*- coding: utf-8 -*-

"""
"""

__author__ = 'stao'

from blinker import Device


async def ready_func():
    await device.saveTextData("hello, blinker")


device = Device("authKey", ready_func=ready_func)

if __name__ == '__main__':
    device.run()
