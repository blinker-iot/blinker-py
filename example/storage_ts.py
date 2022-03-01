# -*- coding: utf-8 -*-

"""
"""

__author__ = 'stao'

import random

from blinker import Device


async def ready_func():
    while True:
        print("save ts data...")
        data = {
            "humi": random.randint(0, 300),
            "temp": random.randint(0, 100)
        }

        await device.saveTsData(data)


device = Device("authKey", protocol="mqtts", ready_func=ready_func)

if __name__ == '__main__':
    device.run()
