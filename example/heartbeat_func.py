# -*- coding: utf-8 -*-

"""
"""

__author__ = 'stao'

from blinker import Device


async def heartbeat_func(msg):
    print("Heartbeat received msg: {0}".format(msg))


device = Device("authKey", heartbeat_func=heartbeat_func)

if __name__ == '__main__':
    device.run()
