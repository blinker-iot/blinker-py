# -*- coding: utf-8 -*-

"""
日志存储示例
"""

__author__ = 'stao'

from blinker import Device, Storage


def save_log_data():
    storage = Storage(device)
    while True:
        log = "Test log"
        storage.save_log(log)


device = Device("authKey", protocol="mqtts", init_ready_func=save_log_data)

if __name__ == '__main__':
    device.run()
