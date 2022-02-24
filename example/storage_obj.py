# -*- coding: utf-8 -*-

"""
"""

__author__ = 'stao'

from blinker import Device, Storage


def save_obj_data():
    storage = Storage(device)
    storage.save_obj({"testKey1": "test1", "testKey2": "test2"})
    print("save ok")


device = Device("authKey", protocol="mqtts", init_ready_func=save_obj_data)

if __name__ == '__main__':
    device.run()
