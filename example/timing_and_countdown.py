# -*- coding: utf-8 -*-

"""
定时和倒计时
"""

__author__ = 'stao'

from blinker import Device


async def builtin_switch_func(msg):
    print("received msg: {0}".format(msg))


device = Device("authKey", builtin_switch_func=builtin_switch_func)

if __name__ == '__main__':
    device.run()
