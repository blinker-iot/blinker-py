# -*- coding: utf-8 -*-

"""
微信模板通知
"""

__author__ = 'stao'

from blinker import Device, Notice


def send_wechat_msg():
    notice = Notice(device)
    notice.wechat(title="消息测试", state="异常", text="设备1出现异常")


device = Device("authKey", protocol="mqtts", init_ready_func=send_wechat_msg)

if __name__ == '__main__':
    device.run()
