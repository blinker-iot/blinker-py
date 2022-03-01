#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "stao"

from blinker import Device, ButtonWidget, NumberWidget

device = Device("authKey")

button1 = device.add_widget(ButtonWidget('btn-123'))
button2 = device.add_widget(ButtonWidget('btn-abc'))
number1 = device.add_widget(NumberWidget('num-abc'))

num = 0


def button1_callback(msg):
    global num

    num += 1

    number1.text("num")
    number1.value(num).update()


def button2_callback(msg):
    print("Button2: {0}".format(msg))


async def heartbeat_test():
    print("Heartbeat test")


async def ready_func():
    # 获取设备配置信息
    print(vars(device.config))


button1.func = button1_callback
button2.func = button2_callback
device.heartbeat_callable = heartbeat_test
device.ready_callable = ready_func

if __name__ == '__main__':
    device.run()
