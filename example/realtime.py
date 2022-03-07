# -*- coding: utf-8 -*-

"""
实时数据
"""

__author__ = 'stao'

import random

from blinker import Device


def generate_data():
    return random.randint(1, 100)


async def realtime_func(keys):
    print("realtime func received {0}".format(keys))
    for key in keys:
        if key == "humi":
            await device.sendRtData(key, generate_data)
        elif key == "temp":
            await device.sendRtData(key, generate_data)


device = Device("authKey", realtime_func=realtime_func)

if __name__ == '__main__':
    device.run()
