# -*- coding: utf-8 -*-

"""
"""

__author__ = 'stao'

import random

from blinker import Device, Storage


# 时序数据存储
def save_ts_data():
    storage = Storage(device)
    while True:
        print("save ts data...")
        data = {
            "humi": random.randint(0, 300),
            "temp": random.randint(0, 100)
        }

        storage.save_ts(data)


device = Device("authKey", protocol="mqtts", init_ready_func=save_ts_data)


if __name__ == '__main__':
    device.run()
