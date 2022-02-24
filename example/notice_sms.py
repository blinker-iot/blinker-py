# -*- coding: utf-8 -*-

"""
短信通知
"""

__author__ = 'stao'

from blinker import Device, Notice


def send_sms():
    notice = Notice(device)
    notice.sms("短信消息测试")


device = Device("authKey", protocol="mqtts", init_ready_func=send_sms)

if __name__ == '__main__':
    device.run()
