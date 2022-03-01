# -*- coding: utf-8 -*-

"""
MQTT消息发送
"""

__author__ = 'stao'

from blinker import Device


async def ready_func():
    msg = {"abc": 123}
    to_device = "设备名"
    await device.sendMessage(msg, to_device)


device = Device("authKey", protocol="mqtts", ready_func=ready_func)

if __name__ == '__main__':
    device.run()
