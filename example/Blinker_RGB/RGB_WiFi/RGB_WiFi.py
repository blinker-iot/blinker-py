#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Blinker import *

auth = 'Your Device Secret Key'

BLINKER_DEBUG.debugAll()

Blinker.mode(BLINKER_WIFI)
Blinker.begin(auth)

rgb1 = BlinkerRGB("RGBKey")

def rgb1_callback(r_value, g_value, b_value, bright_value):
    """ """

    BLINKER_LOG("R value: ", r_value)
    BLINKER_LOG("G value: ", g_value)
    BLINKER_LOG("B value: ", b_value)
    BLINKER_LOG("Brightness value: ", bright_value)

def data_callback(data):
    BLINKER_LOG("Blinker readString: ", data)

    rgb1.brightness(random.randint(0,255))
    rgb1.print(random.randint(0,255), random.randint(0,255), random.randint(0,255))

rgb1.attach(rgb1_callback)
Blinker.attachData(data_callback)

if __name__ == '__main__':

    while True:
        Blinker.run()
