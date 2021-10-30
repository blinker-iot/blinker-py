#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "stao"

from loguru import logger
from blinker import Device, ButtonWidget, NumberWidget

device = Device("", protocol="mqtts")

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
    logger.info("Button2: {0}".format(msg))


button1.func = button1_callback
button2.func = button2_callback

if __name__ == '__main__':
    device.run()
