# -*- coding: utf-8 -*-

"""
MQTT消息发送
"""

__author__ = 'stao'

from blinker import Device


def send_mqtt_msg():
    msg = {"abc": 123}
    to_device = "设备识别码"
    device.mqtt_client.send_to_device(msg, to_device)


device = Device("authKey", protocol="mqtts", init_ready_func=send_mqtt_msg)

if __name__ == '__main__':
    device.run()
