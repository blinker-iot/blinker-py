# -*- coding: utf-8 -*-

"""
通知
"""

__author__ = 'stao'

from blinker import Device


async def ready_func():
    await device.sendSms("test")
    await device.wechat(title="消息测试", state="异常", text="设备1出现异常")


device = Device("authKey", protocol="mqtts", ready_func=ready_func)

if __name__ == '__main__':
    device.run()
